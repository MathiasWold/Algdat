""" LCS and Rod Cutting implemented using dynamic programming (bottom up) """

import sys


def LCS(x, y):
    """ Finds the longest common subsequence of two input sequences """

    n = len(x)
    m = len(y)
    # each cell contains two objects; length and where it got it lenght from
    # u = up, l = left, ul = upleft (diagonally)
    result = [[[0, "  "] for i in range(m+1)] for i in range(n+1)]
    lcs = ""

    for row in range(1, n + 1):
        for col in range(1, m + 1):
            if (x[row - 1] == y[col - 1]):
                # equal symbols
                result[row][col][0] = result[row - 1][col - 1][0] + 1
                result[row][col][1] = "ul"
            else:
                # symbols not equal
                # result[row][col] = max(result[row - 1][col], result[row][col - 1])
                if result[row - 1][col][0] >= result[row][col - 1][0]:
                    result[row][col][0] = result[row - 1][col][0]
                    result[row][col][1] = "u "
                else:
                    result[row][col][0] = result[row][col - 1][0]
                    result[row][col][1] = "l "
    # print sequence:
    for row in result:
        print(row)
    row = n
    col = m
    while row > 0 and col > 0:
        if result[row][col][1] == "ul":
            row -= 1
            col -= 1
            lcs += y[col]
        elif result[row][col][1] == "u ":
            row -= 1
        else:
            col -= 1
    lcs = lcs[::-1]
    print(f"LCS: {lcs}")
    print(f"LCS length: {result[n][m][0]}")


x = list("stone")
y = list("longest")
LCS(x, y)


def rod_cut(prices, length):
    """ 
        Finds the optimal way to cut a rod of length n into smaller pieces such that
        total sell value for all the pieces are maximal
    """

    n = length
    result = [0] * (n + 1)
    cuts = [0] * (n + 1)

    for i in range(1, n + 1):
        q = -sys.maxsize
        for j in range(1, i + 1):
            if q < p[j] + result[i - j]:
                q = p[j] + result[i - j]
                cuts[i] = j
        result[i] = q

    print("Optimal value for rods of size equal to index i: ", result)
    print("First cut to make at index i to construct an optimal solution:", 
    cuts)
    print(f"To get max value with a rod of length {n}, cut pieces of size ", end="")
    while n > 0:
        print(cuts[n], end=", ")
        n = n - cuts[n]
    print(f"which gives a total value of {result[-1]}")


# prices for selling rods of length equal to index of p
p = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
rod_cut(p, 10)
rod_cut(p, 7)
