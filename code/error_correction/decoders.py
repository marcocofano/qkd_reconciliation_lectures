import itertools
import scipy as sp
from scipy.sparse import coo_matrix
import numpy as np

def mtx_to_vec(mtx: coo_matrix):
    return np.asarray(mtx).ravel()

def sum_axis(coo: coo_matrix, axis: int):
    return mtx_to_vec(coo.sum(axis=axis))

# np.sign like func with no zeros returned
def sign(val):
    return (val >= 0).astype(int) * 2 - 1

def assign_data(mat_, d_):
    mat_.data = d_
    return mat_


# all binary_vectors of given length in a matrix
def binary_vectors(length):
    if 0:
        d = np.arange(2 ** length)
        return ((d[:, None] & (1 << np.arange(length))) > 0).astype(int)
    else:
        str_seq = [seq for seq in itertools.product("01", repeat=length)]
        return np.array(str_seq).astype(np.int)


def pseudo_to_cw(x_, allow_pseudo, eps=1e-8):
    if allow_pseudo:
        x_[x_ < eps] = 0
        x_[1 - x_ < eps] = 1
        return x_
    else:
        return (x_ > .5).astype(int)


# input should be a coo_sparse mtx
def prod_nonzero_sign(coo, axis):
    temp = coo.data
    coo.data = coo.data < 0
    out = (mtx_to_vec(coo.sum(axis=axis)) % 2) * -2 + 1
    coo.data = temp
    return out


# input should be a coo_sparse mtx, axis= 0 cols, 1 rows
def prod_nonzero(coo, axis):
    temp = coo.data  # reusing existing coo without creating new one
    coo.data = np.log(np.abs(coo.data))
    mag = np.exp(mtx_to_vec(coo.sum(axis=axis)))
    coo.data = temp
    return prod_nonzero_sign(coo, axis) * mag


# wrapper to avoid the warning from np.arctanh(1 or -1)
def arctanh(val, out):
    ind_inf = np.abs(val) == 1
    out[ind_inf] = np.inf * val[ind_inf]
    out[~ind_inf] = np.arctanh(val[~ind_inf])
    return out


def log_sum_exp_rows(arr):
    arr_max = arr.max(axis=1)
    return arr_max + np.log(np.exp(arr - arr_max[:, None]).sum(axis=1))


# returns a random element if encountered multiple arg maxes
def arg_max_rand(values):
    max_ind = np.argwhere(values == np.max(values))
    return np.random.choice(max_ind.flatten(), 1)[0]


# https://stackoverflow.com/questions/30742572/argmax-of-each-row-or-column-in-scipy-sparse-matrix
def csr_csc_argmax(X, axis=None):
    is_csr = isinstance(X, sp.csr_matrix)
    is_csc = isinstance(X, sp.csc_matrix)
    assert (is_csr or is_csc)
    assert (not axis or (is_csr and axis == 1) or (is_csc and axis == 0))

    major_size = X.shape[0 if is_csr else 1]
    major_lengths = np.diff(X.indptr)  # group_lengths
    major_not_empty = (major_lengths > 0)

    result = -np.ones(shape=(major_size,), dtype=X.indices.dtype)
    split_at = X.indptr[:-1][major_not_empty]
    maxima = np.zeros((major_size,), dtype=X.dtype)
    maxima[major_not_empty] = np.maximum.reduceat(X.data, split_at)
    all_argmax = np.flatnonzero(np.repeat(maxima, major_lengths) == X.data)
    result[major_not_empty] = X.indices[all_argmax[np.searchsorted(all_argmax, split_at)]]
 
class BPA:

    def __init__(self, parity_mtx, max_iter: int = 10):
        self.max_iter = max_iter
        if parity_mtx is None:
            raise ValueError("Parity Check matrix cannot be None")
        self.parity_mtx = parity_mtx
        self.xx, self.yy = np.where(self.parity_mtx)

        self.coo = lambda d_: coo_matrix((d_, (self.xx, self.yy)), shape=parity_mtx.shape)
        self.sum_cols = lambda d_: sum_axis(self.coo(d_), 0)

    def decode(self, y, priors):
        xx, yy, sum_cols = self.xx, self.yy, self.sum_cols
        var_to_chk, chk_to_var = priors[yy], priors[yy]
        x_hat, iter_count = y, 0

        def ret(val):
            # print(val, ':', iter_count)
            return x_hat

        while 1:
            if 0 < self.max_iter <= iter_count:
                return x_hat, iter_count, False
            if ((self.parity_mtx @ x_hat) % 2 == 0).all(): 
                return x_hat, iter_count, True

            # chk_to_var
            self.decode_(var_to_chk, xx, chk_to_var)

            # var_to_chk
            marginal = priors + sum_cols(chk_to_var)
            if 1:
                var_to_chk = marginal[yy] - chk_to_var
                marginal[np.isnan(marginal)] = 0.
            else:
                # TODO: following piece is to handle cases where llr is inf. slower and uglier than inf unhandled case. needs refactoring
                # assert fails on (inf-inf), i.e., conflicting 100% beliefs form checks
                # may be replace them by 0 cuz conflicting certainties mean uncertain?
                # assert (~np.isnan(marginal).any())
                marginal[np.isnan(marginal)] = 0.
                mar_yy = marginal[yy]

                inf_ind = np.abs(chk_to_var) == np.inf
                sums = sum_cols(inf_ind)
                ma_0, ma_1, ma_2 = (sums == 0)[yy], (sums == 1)[yy], (sums >= 2)[yy]
                # cols with 0 inf elements
                var_to_chk[ma_0] = mar_yy[ma_0] - chk_to_var[ma_0]
                # cols with 1 or more +-inf elements get +-inf
                var_to_chk[~ma_0] = mar_yy[~ma_0] - 0.

                # cols with 1 +-inf element
                chk_to_var[inf_ind] = 0.
                chk_to_var_inf = (priors + sum_cols(chk_to_var))[yy]
                ma_1 = np.logical_and(ma_1, inf_ind, out=ma_1)
                var_to_chk[ma_1] = chk_to_var_inf[ma_1]

            # bitwise decoding
            x_hat = (marginal < 0).astype(int)
            iter_count += 1


class SPA(BPA):
    name =  "spa"

    def __init__(self, parity_mtx, max_iter):
        super().__init__(parity_mtx, max_iter)
        self.prod_rows = lambda d_: prod_nonzero(self.coo(d_), 1)

    def decode_(self, var_to_chk, xx, chk_to_var):
        tanned = np.tanh(var_to_chk / 2.)
        chk_msg_prod = self.prod_rows(tanned)
        tan = chk_msg_prod[xx] / tanned  # TODO: handle possible div by 0
        chk_to_var[:] = 2 * arctanh(tan, out=chk_to_var)

def decoder_factory(decoder_name):
    decoders_dict = {"spa": SPA}
    return decoders_dict.get(decoder_name)

# class MSA(BPA):
#     def __init__(self, parity_mtx, **kwargs):
#         super().__init__(parity_mtx, **kwargs)
#         self.sign_rows = lambda d_: prod_nonzero_sign(self.coo(d_), 1)
#         self.to_csr = lambda d_: self.coo(d_).tocsr()
#         self.min_rows = lambda csr: csr_csc_argmax(-csr)
#         self.row_ind = np.array(range(parity_mtx.shape[0]))
#
#     def decode_(self, var_to_chk, xx, chk_to_var):
#         # TODO: way slower than SPA. needs refactoring
#         sign = self.sign_rows(var_to_chk)[xx] / sign(var_to_chk)
#         csr = self.to_csr(np.abs(var_to_chk))
#         chk_to_var_csr = self.to_csr(chk_to_var)
#         arg_min_1 = self.min_rows(csr)
#         min_ind_1 = self.row_ind, arg_min_1
#         min_val_1 = mtx_to_vec(csr[min_ind_1])
#         chk_to_var_csr.data[:] = min_val_1[xx]
#
#         csr[min_ind_1] = np.inf
#         arg_min_2 = self.min_rows(csr)
#         min_ind_2 = self.row_ind, arg_min_2
#         min_val_2 = mtx_to_vec(csr[min_ind_2])
#         chk_to_var_csr[min_ind_1] = min_val_2
#
#         chk_to_var[:] = sign * chk_to_var_csr.data
