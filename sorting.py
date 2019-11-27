""" Sorting (Divide and Conquer and in linear time) and Order Statistics """

import sys
import random


def insertion_sort(A):
    """ Sorts A by inserting elements into the right place of the array, one after one """

    for i in range(1, len(A)):
        key = A[i]
        j = i - 1
        while j >= 0 and A[j] > key:
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = key


def merge(A, start_index, split_index, end_index):
    """ 
        Merges two subarrays by inserting their elements into the main array by comparing 
        elements at one index at a time, assuming the subarrays are already sorted 
    """

    # number of elements in [0 ... split_index] and [split_index + 1 ... end_index]
    n = split_index - start_index + 1
    m = end_index - split_index

    # left and right subarrays
    L = [0] * (n + 1)
    R = [0] * (m + 1)

    # fills the left subarray [0 ... split_index]
    for i in range(n):
        L[i] = A[start_index + i]

    # fills the right subarray [split_index + 1 ... end_index]
    for i in range(m):
        R[i] = A[split_index + 1 + i]

    # last element of each subarray = inf to make sure
    # all elements from both sub-arrays gets inserted into the main array by the comparison below
    L[n] = R[m] = sys.maxsize

    # indexes for left and right subarray, the indexes represent the next element to extract from subarray
    # into the main array
    i = j = 0

    for k in range(start_index, end_index + 1):
        # If item L[i] in left subarray is less than or equal to element R[j] in right array,
        # add L[i] to main array, else do the opposite.
        # Also increase index to the subarray we got the element from, since the element now is
        # inserted into the main array and we want to look at the next element in the subbaray.
        if L[i] <= R[j]:
            A[k] = L[i]
            i += 1
        else:
            A[k] = R[j]
            j += 1


def merge_sort(A, start_index, end_index):
    """ Sorts A recursively by splitting to subarrays and then merging them """

    if start_index < end_index:
        split_index = int((start_index + end_index)/2)
        merge_sort(A, start_index, split_index)
        merge_sort(A, split_index + 1, end_index)
        merge(A, start_index, split_index, end_index)


def partion(A, start_index, end_index):
    """ Returns an index which splits A into two partitions """

    x = A[end_index]  # pivot

    # indexes less than or equal to i contains values less than or equal to x
    i = start_index - 1

    for j in range(start_index, end_index):
        if A[j] <= x:
            # if current index j is less than or equal to pivot, move it to the right partition
            # and add 1 ti index i (since we got another number less than or equal to x)
            i = i + 1
            A[i], A[j] = A[j], A[i]

    # swaps the last element with i + 1, such that A is correctly partitioned as
    # A[start_index ... i + 1] and A[i + 2 ... end_index]
    A[i + 1], A[end_index] = A[end_index], A[i+1]

    return i + 1


def quicksort(A, start_index, end_index):
    """ Uses partitioning to sort an array recursively """

    if start_index < end_index:
        pivot = partion(A, start_index, end_index)
        quicksort(A, start_index, pivot - 1)
        quicksort(A, pivot + 1, end_index)


def randomized_partition(A, start_index, end_index):
    """ Same as partition, but uses a random element as pivot instead of always using the last element """

    pivot = random.randint(start_index, end_index)

    # swap pivot with last elemente such that we can run partition
    # with a new (random) last element as pivot
    A[pivot], A[end_index] = A[end_index], A[pivot]

    return partion(A, start_index, end_index)


def randomized_quicksort(A, start_index, end_index):
    """
        Same as quicksort, but with a random pivot chosen at each
        partition instead of always using the last element
    """
    if start_index < end_index:
        pivot = randomized_partition(A, start_index, end_index)
        randomized_quicksort(A, start_index, pivot - 1)
        randomized_quicksort(A, pivot + 1, end_index)


def randomized_select(A, start_index, end_index, order):
    """ Returns the element in A that is larger than exactly (order - 1) other elements of A """

    if start_index == end_index:
        return A[start_index]

    pivot = randomized_partition(A, start_index, end_index)

    # the number k of elements in the subarray A[start_index ... pivot],
    # that is, the number of elements in the low side of the partition, plus one for the pivot element
    k = pivot - start_index + 1
    if order == k:  # the pivot value is the answer
        return A[pivot]
    elif order < k:
        return randomized_select(A, start_index, pivot - 1, order)
    else:
        return randomized_select(A, pivot + 1, end_index, order - k)


def counting_sort(A, max_int_value):
    """ Sorts integers in range [0 ... max_int_value] by counting """

    # B stores the result, C counts elements
    B = [0] * len(A)
    C = [0] * (max_int_value + 1)

    # computes C, where C[i] contains the number of elements equal to i
    for i in range(len(A)):
        C[A[i]] += 1

    # makes C contain the number of elements less than or equal to i
    for i in range(1, max_int_value + 1):
        C[i] += C[i - 1]

    for i in range(len(A) - 1, 0, -1):
        B[C[A[i]] - 1] = A[i]
        C[A[i]] -= 1

    return B


def bucket_sort(A):
    """ 
        Sorts A using bucket-distribution, assumes that the elements of A have a
        uniform distribution (in the range [0, 1))
    """

    n = len(A)
    B = [None] * n
    for i in range(n):
        B[i] = []

    # distribute numbers into buckets
    for i in range(1, n):
        B[int(n * A[i - 1])].append(A[i - 1])

    result = []
    # sort each bucket (the elemenets should be evenly distributed in
    # the buckets assuming input of a uniform distribution)
    for i in range(n):
        insertion_sort(B[i])
        result += B[i]

    return result


def test1():
    """ Test for quicksort and randomized quicksort """
    a = [2, 8, 7, 1, 6, 3, 5, 6, 4]
    #quicksort(a, 0, len(a) - 1)
    randomized_quicksort(a, 0, len(a) - 1)
    print(a)

# test1()


def test2():
    """ Test for randomized-select """
    a = [2, 8, 7, 1, 6, 5, 4]
    result = randomized_select(a, 0, len(a) - 1, 6)
    quicksort(a, 0, len(a) - 1)
    print(a)
    print(result)

# test2()


def test3():
    """ Test for counting-sort """
    a = [1, 4, 7, 5, 3, 2, 5, 5, 5, 3, 4, 3, 8,
         7, 6, 5, 21, 2, 1, 2, 23, 13, 15, 0, 2]
    print(counting_sort(a, 23))

# test3()


def test4():
    """ Test for bucket-sort and insertion sort """
    a = [.78, .17, .39, .26, .72, .94, .21, .12, .23, .68]
    print(bucket_sort(a))


# test4()

def test5():
    """ Test for merge-sort """
    a = [1, 4, 7, 5, 3, 2, 5, 5, 5, 3, 4, 3, 8,
         7, 6, 5, 21, 2, 1, 2, 23, 13, 15, 0, 2]
    merge_sort(a, 0, len(a) - 1)
    print(a)


test5()
