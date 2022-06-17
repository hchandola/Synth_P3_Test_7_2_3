from typing import List


def sat303(strategies: List[List[float]], A=[[1.0, -1.0], [-1.3, 0.8]], B=[[-0.9, 1.1], [0.7, -0.8]], eps=0.01):
    m, n = len(A), len(A[0])
    p, q = strategies
    assert len(B) == m and all(len(row) == n for row in A + B), "inputs are a bimatrix game"
    assert len(p) == m and len(q) == n, "solution is a pair of strategies"
    assert sum(p) == sum(q) == 1.0 and min(p + q) >= 0.0, "strategies must be non-negative and sum to 1"
    v = sum(A[i][j] * p[i] * q[j] for i in range(m) for j in range(n))
    w = sum(B[i][j] * p[i] * q[j] for i in range(m) for j in range(n))
    return (all(sum(A[i][j] * q[j] for j in range(n)) <= v + eps for i in range(m)) and
            all(sum(B[i][j] * p[i] for i in range(m)) <= w + eps for j in range(n)))
def sol303(A=[[1.0, -1.0], [-1.3, 0.8]], B=[[-0.9, 1.1], [0.7, -0.8]], eps=0.01):
    """
    Find an eps-Nash-equilibrium for a given two-player game with payoffs described by matrices A, B.
    For example, for the classic Prisoner dilemma:
       A=[[-1., -3.], [0., -2.]], B=[[-1., 0.], [-3., -2.]], and strategies = [[0, 1], [0, 1]]

    eps is the error tolerance
    """
    NUM_ATTEMPTS = 10 ** 5

    def sat303(strategies: List[List[float]], A, B, eps):
        m, n = len(A), len(A[0])
        p, q = strategies
        assert len(B) == m and all(len(row) == n for row in A + B), "inputs are a bimatrix game"
        assert len(p) == m and len(q) == n, "solution is a pair of strategies"
        assert sum(p) == sum(q) == 1.0 and min(p + q) >= 0.0, "strategies must be non-negative and sum to 1"
        v = sum(A[i][j] * p[i] * q[j] for i in range(m) for j in range(n))
        w = sum(B[i][j] * p[i] * q[j] for i in range(m) for j in range(n))
        return (all(sum(A[i][j] * q[j] for j in range(n)) <= v + eps for i in range(m)) and
                all(sum(B[i][j] * p[i] for i in range(m)) <= w + eps for j in range(n)))

    import random
    r = random.Random(0)
    dims = len(A), len(A[0])
    # possible speedup: remove dominated strategies
    for _attempt in range(NUM_ATTEMPTS):
        strategies = []
        for d in dims:
            s = [max(0.0, r.random() - 0.5) for _ in range(d)]
            tot = sum(s) + 1e-6
            for i in range(d):
                s[i] = (1.0 - sum(s[:-1])) if i == d - 1 else (s[i] / tot)  # to ensure sum is exactly 1.0
            strategies.append(s)
        if sat303(strategies, A, B, eps):
            return strategies
# assert sat303(sol303())

