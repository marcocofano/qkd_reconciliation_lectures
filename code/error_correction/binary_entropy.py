import numpy as np
import argparse

def h_inverse(y):
    """Inverse of binary entropy"""
    #TODO: Review this formula, not working
    return np.log(1+np.sqrt(1- y**(4/3) + (y-1)*np.log(2))) / (2*np.atanh(np.sqrt(y**(4/3) + (y-1)*np.log(2))))

def binary_entropy(p):
    # Avoid issues with log(0) by using np.where
    p = np.clip(p, 1e-12, 1-1e-12)
    return -p * np.log2(p) - (1-p) * np.log2(1-p)

def binary_entropy_prime(x):
    """
    Derivative of the binary entropy (in bits):
        H2'(x) = ln((1-x)/x) / ln(2)
    """
    # Be careful with edge cases x=0 or x=1 in practice
    return np.log((1.0 - x)/x) / np.log(2.0)

def binary_entropy_inverse_newton(y, tol=1e-12, max_iter=50):
    """
    Invert the binary entropy function for y in [0, 1].
    Returns the x in [0, 0.5] such that H2(x) = y.
    
    Uses the approximate formula x0 = 1/2(1 - sqrt(1 - y^(4/3)))
    as the initial guess, followed by Newton's iteration.
    """
    # # Edge cases:
    if y <= 0.0:
        return 0.0  # H2(0) = 0
    if y >= 1.0:
        return 0.5  # H2(0.5) = 1
    
    # 1) Initial guess using the approximation
    x = 0.5 * (1.0 - np.sqrt(1.0 - y**(4.0/3.0)))
    
    # 2) Newton iteration
    for _ in range(max_iter):
        f  = binary_entropy(x) - y
        fp = binary_entropy_prime(x)
        # If derivative is too small or we are close enough, break
        if abs(f) < tol or abs(fp) < 1e-15:
            break
        x_new = x - f/fp
        # Keep x in [0,0.5] (we want the 'lower' branch)
        x = max(0.0, min(0.5, x_new))
    
    return x

def coderate_from_params(p, f):
    return 1. - f * binary_entropy(p)

def efficiency_from_params(p, cr):
    return (1. - cr)/binary_entropy(p)

def crossprob_from_params(f, cr):
    binary_entropy_inverse = np.vectorize(binary_entropy_inverse_newton, otypes=[np.float64])
    return binary_entropy_inverse((1-cr)/f)

def main():
    parser = argparse.ArgumentParser()
    commands =  parser.add_subparsers(dest="command")

    coderate_parser = commands.add_parser("coderate")
    coderate_parser.add_argument("--p", type=float, help="crossover probability", default=0.1)
    coderate_parser.add_argument("--f", type=float, help="efficiency", default=1.12 )

    crossprob_parser = commands.add_parser("crossprob")
    crossprob_parser.add_argument("--cr", type=float, help="coderate", default=0.1)
    crossprob_parser.add_argument("--f", type=float, help="efficiency", default=1.12 )

    args = parser.parse_args()

    if args.command == "coderate":
        print(coderate_from_params(args.p, args.f))
    elif args.command == "crossprob":
        print(crossprob_from_params(args.cr, args.f))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
