import numpy as np
import argparse
from dataclasses import dataclass
from typing import Optional
import scipy as sp
from scipy.sparse import coo_matrix
from pathlib import Path
from collections import Counter

from error_correction.data_dirs import ErrorCorrectionDirs


@dataclass
class CodeConfig:
    format: str
    code_length: int
    name: str
    seed: int

    def get_slug(self):
        return f"{self.format}_{self.code_length}_{self.name}_{self.seed}"

    @classmethod
    def from_slug(cls, slug):
        slug_list = slug.split("_")
        return cls(
            format=slug_list[0],
            code_length=slug_list[1],
            name=slug_list[2],
            seed=slug_list[3],
        )


class Code:
    def __init__(
        self,
        config: CodeConfig,
        parity_mtx: Optional[coo_matrix],
        data_dirs: ErrorCorrectionDirs = ErrorCorrectionDirs(),
    ):
        if parity_mtx is not None:
            self.parity_mtx = parity_mtx
        self.config = config
        self.data_dirs = data_dirs

    # @staticmethod
    # def check_gen_matrix()
    #     if gen_mtx is not None:
    #     k, n = gen_mtx.shape
    #     messages = mu.binary_vectors(k)
    #     cb = (messages @ gen_mtx) % 2
    #
    #     # check if GH^T = 0
    #     assert (np.sum((self.cb @ parity_mtx.T) % 2) == 0)
    #     assert (self.cb[0].sum() == 0)  # all zeros cw
    #     # assert (self.cb[-1].sum() == n)  # all ones cw

    def gen_matrix(self):
        pass

    @classmethod
    def from_config(
        cls,
        config: Optional[CodeConfig],
        data_dirs: ErrorCorrectionDirs = ErrorCorrectionDirs(),
    ):
        """Initializer of Code from a CodeConfig specification.
        It tries to find a H matrix with the specified conf.

        Raises: FileNotFoundError, if H matrix is not in file_codes_dir
        """
        if not config:
            raise ValueError("Config needed to initialize code")
        filename = config.get_slug()

        file_path = data_dirs.code_path(filename)
        parity_mtx = load_parity_mtx(file_path)
        return cls(config, parity_mtx, data_dirs)

    def get_filepath(self) -> Path:
        return self.data_dirs.output_path(f"{self.config.get_slug()}")

    def save_code(self):
        """Saves the code H matrix in COO format, as a text file"""
        file_path = self.get_filepath()
        with open(file_path, "w") as fp:
            for chk_ind in range(self.parity_mtx.shape[0]):
                ind = np.where(self.parity_mtx[chk_ind, :])[0] + 1
                fp.writelines(" ".join(map(str, ind)) + "\n")

    def get_k(self) -> int:
        """Number of parity bits / check equations"""
        return self.get_n() - self.parity_mtx.shape[0]

    def get_n(self) -> int:
        """Code length"""
        return self.parity_mtx.shape[1]

    def code_rate(self) -> float:
        return (self.get_n() - self.get_k()) / self.get_n()

    def compute_density(self) -> float:
        """Computes density for a given NumPy array or SciPy sparse matrix."""
        if isinstance(self.parity_mtx, np.ndarray):
            total_elements = self.parity_mtx.size
            nonzero_elements = np.count_nonzero(self.parity_mtx)
        return nonzero_elements / total_elements if total_elements > 0 else 0

    def compute_degree_distribution(self) -> dict:
        """
        Computes the degree distribution of check nodes (rows) and variable nodes (columns)
        in a Tanner graph.

        Parameters:
            sparse_matrix (scipy.sparse.coo_matrix): The Tanner graph adjacency matrix.

        Returns:
            dict: Degree distributions for check nodes and variable nodes.
        """
        # if type(self.parity_mtx) is np.ndarray:
        #     rows, cols = np.nonzero(self.parity_mtx)  # Get nonzero indices
        #     data = np.ones(len(rows), dtype=int)  # All nonzero values are 1
        #     shape = self.parity_mtx.shape  # Preserve original shape
        #
        #     sparse_matrix = coo_matrix((data, (rows, cols)), shape=shape)

        # Compute row degrees (Check nodes: how many variable nodes they connect to)
        check_node_degrees = np.array(self.parity_mtx.sum(axis=1)).flatten()

        # Compute column degrees (Variable nodes: how many check nodes they connect to)
        variable_node_degrees = np.array(self.parity_mtx.sum(axis=0)).flatten()

        # Count occurrences of each degree
        check_node_degree_distribution = dict(Counter(check_node_degrees))
        variable_node_degree_distribution = dict(Counter(variable_node_degrees))

        return {
            "check_node_distribution": check_node_degree_distribution,
            "variable_node_distribution": variable_node_degree_distribution,
        }

def save_parity_mtx(matrix, filepath, in_format=None, out_format=None):
    file_path = f"{filepath}"
    with open(file_path, "w") as f:
        for row in matrix:
            # Find indices where the element is 1, convert them to 1-based indexing
            cols = np.where(row == 1)[0] + 1
            # Join the indices into a space separated string
            line = " ".join(map(str, cols))
            f.write(line + "\n")



def load_parity_mtx(filepath):
    file_path = f"{filepath}"
    with open(file_path, "r") as fp:
        lines = tuple(line for line in fp if len(line.split()) > 0)
        max_ind = max(tuple(max(map(int, line.split())) for line in lines))
        min_ind = min(tuple(min(map(int, line.split())) for line in lines))
        if min_ind not in [0, 1]:
            raise Exception("Minimum index is not 0 or 1.")
        mtx = np.zeros((len(lines), max_ind + (0 if min_ind == 1 else 1)), int)
        chk_num = 1
        for line in lines:
            for var_num in map(int, line.split()):
                mtx[chk_num - 1, var_num - 1] = 1
            chk_num += 1
        return mtx


def rand_reg_ldpc(n, l, r):
    m = int(n * l / r)
    parity_mtx = np.zeros((m, n), int)
    var_ind = np.arange(n)
    rand_numb = np.random.randint(1, 100)
    for i in range(m):
        pairs = list(zip(parity_mtx.sum(axis=0), var_ind))
        np.random.shuffle(pairs)
        pairs.sort(key=lambda x: x[0])
        ind = np.array(list(zip(*pairs))[1])
        parity_mtx[i, ind[0:r]] = 1
    assert (parity_mtx.sum(axis=0) == l).all()
    assert (parity_mtx.sum(axis=1) == r).all()
    return  parity_mtx # np.sort(H @ (2 ** var_ind))


def rand_reg_ldpc_improved(n,l,r):
    m = int(n * l / r)
    parity_mtx = np.zeros((m, n), dtype=int)
    col_degrees = np.zeros(n, dtype=int)  # running count of 1's per column

    for i in range(m):
        # Generate a random array for tie-breaking.
        # np.lexsort sorts by the last key first, so we pass (random, col_degrees)
        random_keys = np.random.random(n)
        order = np.lexsort((random_keys, col_degrees))
        
        # Choose the first r columns from the sorted order
        selected = order[:r]
        parity_mtx[i, selected] = 1
        
        # Update the column degrees
        col_degrees[selected] += 1

    # Verification (optional)
    assert (col_degrees == l).all(), "Each column must have exactly l ones."
    assert (parity_mtx.sum(axis=1) == r).all(), "Each row must have exactly r ones."
    
    return parity_mtx

def rand_reg_ldpc_test():
    nn = 100
    xx = np.zeros([nn, 6])
    for i in range(nn):
        xx[i, :] = rand_reg_ldpc(12, 3, 6)
    print(xx[xx[:, 0].argsort()])


# def gen_rand_reg_ldpc(args):
#     n, l, r = args.n, args.l, args.r
#     for i in range(args.count):
#         parity_mtx = rand_reg_ldpc(n, l, r)
#         code_name = "%d_%d_%d_rand_ldpc_%d" % (n, l, r, i + 1)
#         save_parity_mtx(parity_mtx, code_name)
#         verify_rand_reg_ldpc(code_name, l, r)


# def verify_rand_reg_ldpc(code_name, l, r):
#     parity_mtx = get_code(code_name).parity_mtx
#     print(
#         parity_mtx.shape,
#         (parity_mtx.sum(axis=0) == l).all(),
#         (parity_mtx.sum(axis=1) == r).all(),
#     )


# find_gen_mtx given parity_mtx, not final version.
def find_gen_mtx():
    H = 0  # copy the parity_mtx of 12_3_4_ldpc code
    all_sets = mu.binary_vectors(12).T
    G = all_sets[:, (H @ all_sets % 2).sum(0) == 0][:, [1, 2, 4, 8, 16]].T
    print(G @ H.T % 2, G.shape)
    print(G)


codes = {
    "4_2_test": (
        np.array(
            [
                [1, 1, 1, 0, 0],  # gen_mtx
                [0, 0, 1, 1, 1],
            ]
        ),
        np.array(
            [
                [1, 1, 0, 0, 0],  # parity_mtx
                [0, 1, 1, 1, 0],
                [0, 0, 0, 1, 1],
            ]
        ),
    ),
    # find gen_mtx using wolframalpha: nullspace of <H> in GF(2)
    "6_2_3_ldpc": (
        np.array(
            [
                [0, 0, 0, 1, 0, 1],  # gen_mtx
                [1, 0, 1, 1, 1, 0],
                [1, 1, 0, 0, 0, 0],
            ]
        ),
        np.array(
            [
                [1, 1, 1, 0, 0, 0],  # parity_mtx
                [0, 0, 0, 1, 1, 1],
                [0, 0, 1, 1, 0, 1],
                [1, 1, 0, 0, 1, 0],
            ]
        ),
    ),
    "7_4_hamming": (
        np.array(
            [
                [1, 1, 1, 0, 0, 0, 0],  # gen_mtx
                [1, 0, 0, 1, 1, 0, 0],
                [0, 1, 0, 1, 0, 1, 0],
                [1, 1, 0, 1, 0, 0, 1],
            ]
        ),
        np.array(
            [
                [0, 0, 0, 1, 1, 1, 1],  # parity_mtx
                [0, 1, 1, 0, 0, 1, 1],
                [1, 0, 1, 0, 1, 0, 1],
            ]
        ),
    ),
    # http://circuit.ucsd.edu/~yhk/ece154c-spr16/pdfs/ErrorCorrectionIII.pdf
    "12_3_4_ldpc": (
        np.array(
            [
                [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
                [0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0],
                [0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
                [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
            ]
        ),
        np.array(
            [
                [0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0],  # parity_mtx
                [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0],
                [0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
                [0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1],
                [1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1],
                [0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0],
            ]
        ),
    ),
}


def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("count", help="number of random codes to generate", type=int)
    parser.add_argument("n", help="regular ldpc code length", type=int)
    parser.add_argument("l", help="l", type=int)
    parser.add_argument("r", help="r", type=int)
    return parser


if __name__ == "__main__":
    gen_rand_reg_ldpc(setup_parser().parse_args())
