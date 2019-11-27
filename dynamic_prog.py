""" LCS and Rod Cutting implemented using dynamic programming (bottom up) """

import sys


def LCS(x, y):
    """ Finds the longest common subsequence of two input sequences """

    n = len(x)
    m = len(y)
    # each cell contains two objects; length and where it got it length from
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


def test1():
    """ Test for LCS """
    x = list("stone")
    y = list("longest")
    LCS(x, y)

# test1()


def rod_cut(prices, length):
    """ 
        Finds the optimal way to cut a rod of length n into smaller pieces such that
        total sell value for all the pieces are maximal
    """

    n = length
    result = [0] * (n + 1)
    cuts = [0] * (n + 1)

    # for rods i of length 1 ... n
    for i in range(1, n + 1):
        # max value we can get for rods of length i
        max_val = -sys.maxsize
        # for cuts of lengths 1 ... i
        for j in range(1, i + 1):
            # if max value is less than the value of a cut of j plus a cut of i - j --> set this sum as new max value for this i
            if max_val < prices[j] + result[i - j]:
                max_val = prices[j] + result[i - j]
                # cuts[i] stores where we had to cut to get max value at a given rod with length i
                cuts[i] = j

        # add the max value we can get for a rod of length i
        result[i] = max_val

    print("Optimal value for rods of size equal to index i: ", result)
    print("First cut to make at index i to construct an optimal solution:",
          cuts)
    print(
        f"To get max value with a rod of length {n}, cut pieces of size ", end="")
    while n > 0:
        print(cuts[n], end=", ")
        n = n - cuts[n]
    print(f"which gives a total value of {result[-1]}")


def test2():
    """ Test for roc_cut """
    # prices for selling rods of length equal to index of p
    p = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
    rod_cut(p, 10)
    rod_cut(p, 7)

# test2()


class Item:
    """ Class for an item with given weight and value, to be used in the 0/1 knapsack problem """

    def __init__(self, weight, value):
        self.weight = weight
        self.value = value


def binary_knapsack(items, W):
    """ Solves the 0/1 knapsack problem with a bottom-up approach using dynamic programming """

    # adding a new "blank" item in front of the original items, to be used for comparison with the first item in the loops below
    items = [Item(0, 0)] + items
    # n items, W is max weight for knapsack
    n = len(items)

    # K holds the max value we can earn by including items 1 ... n with a max weight 0 ... W
    # This is computed and stored in K[i][j] for item i and weight j
    K = [[0 for i in range(W + 1)] for i in range(n)]

    # i = row (item), j = column (weight)
    for i in range(1, n):
        for j in range(W + 1):
            # x = exclude item i = max value for including up to item i - 1 at max weight j
            x = K[i - 1][j]

            # if weight j is less than weight of item i --> we do not have space for item i --> max value stays the same
            if j < items[i].weight:
                K[i][j] = x

            # else weight j is larger than (or equal to) weight of item i
            else:
                # y = include item i = max value for including up to item i - 1 at max weight (j - weight of item i) plus value of item i
                y = K[i - 1][j - items[i].weight] + items[i].value

                # compare max values given by including or excluding item i at weight j, and set K[i][j] as the max of these values
                K[i][j] = max(x, y)

    # remove the first helper-row for the blank item before returning K
    # max value we can get is in the bottom-right-most cell
    return K[1:]


def test3():
    """ Test for binary knapsack """
    a = Item(10, 60)
    b = Item(20, 100)
    c = Item(30, 120)

    items = [a, b, c]
    max_weight = 50
    K = binary_knapsack(items, max_weight)
    for row in K:
        print(row)

    print(f"Max value: {K[len(items) - 1][max_weight]}")


test3()
