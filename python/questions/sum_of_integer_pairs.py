"""
Input  :  arr[] = {1, 5, 7, -1},
          sum = 6
Output :  2
Pairs with sum 6 are (1, 5) and (7, -1)

Input  :  arr[] = {1, 5, 7, -1, 5},
          sum = 6
Output :  3
Pairs with sum 6 are (1, 5), (7, -1) &
                     (1, 5)

Input  :  arr[] = {1, 1, 1, 1},
          sum = 2
Output :  6
There are 3! pairs with sum 2.

Input  :  arr[] = {10, 12, 10, 15, -1, 7, 6,
                   5, 4, 2, 1, 1, 1},
          sum = 11
Output :  9
"""


# Python 3 implementation of simple method
# to find count of pairs with given sum.
# Returns number of pairs in arr[0..n-1]
# with sum equal to 'sum'
def getPairsCount(arr, n, sum):
    m = [0] * 1000

    # Store counts of all elements in map m
    for i in range(0, n):
        m[arr[i]] += 1

    # print(m)
    twice_count = 0

    # Iterate through each element and increment
    # the count (Notice that every pair is
    # counted twice)
    for i in range(0, n):
        print(sum - arr[i])
        twice_count += m[sum - arr[i]]

        # if (arr[i], arr[i]) pair satisfies the
        # condition, then we need to ensure that
        # the count is  decreased by one such
        # that the (arr[i], arr[i]) pair is not
        # considered
        if (sum - arr[i] == arr[i]):
            twice_count -= 1

    # return the half of twice_count
    # print(twice_count)
    # print(m)
    return int(twice_count / 2)


# Driver function
arr = [1, 1, 1, 1]
n = len(arr)
sum = 2

print("Count of pairs is", getPairsCount(arr, n, sum))

arr = [10, 12, 10, 15, -1, 7, 6,
       5, 4, 2, 1, 1, 1]
sum = 11
n = len(arr)
print("Count of pairs is", getPairsCount(arr, n, sum))
