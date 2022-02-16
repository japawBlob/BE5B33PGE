
# [1] (**complexity!**)
# Check if in an array the following holds:
# a) the number of leading values 0 is equal to the number of
#    the trailing values 0 (ex.: 001...100 -- OK, 01...0001 -- bad)
# b) each value 1 is surrounded by values 0 (ex ...010... OK,
# c) each value 1 is followed by at least two values 0.
def checkIfArrayHolds (array, option):
    if option == 'a':
        arrayLen = len(array)
        for i in range(arrayLen):
            if array[i] == 0:
                if array[arrayLen-1-i] == array[i]:
                    continue
                else:
                    return False
            return True
    elif option == 'b':
        arrayLen = len(array)
        if array[0] == 1 or array[arrayLen-1] == 1:
            return False
        for i in range(1,arrayLen-1):
            if array[i] == 1:
                if array[i-1] == 0 and array[i+1] == 0:
                    continue
                else:
                    return False
        return True
    elif option == 'c':
        arrayLen = len(array)
        if array[arrayLen-2] == 1 or array[arrayLen-1] == 1:
            return False
        if array[arrayLen-3] == 1:
            if array[arrayLen-2] != 0 or array[arrayLen-1] != 0:
                return False
        for i in range(arrayLen-3):
            if array[i] == 1:
                if array[i+1] == 0 and array[i+2] == 0:
                    continue
                else:
                    return False
        return True
    else :
        print("please enter valid option argument")
        return False

# [12] (**complexity!**)
# Two indices i < j in an array A are called guards when each element with index
# between i and j is smaller than min(A[i], A[j]). Find all guards in a given array.
# Example: A = [8, 2, 7, 5, 2, 3, 4, 2, 6, 1]
# Guards are 2, 8, because A[2] = 7, A[8] = 6 and all elements between  indices 2 and 8 are smaller than min(A[2], A[8]).


if __name__ == '__main__':
    testArrayOfArrays = [[0,0,0,1,2,1,1,1,0,0,0],[0,1,0,1,1,0,1,0,1,1,0],[0,1,0,1,0,1],[0,1,0,0,0,1,0],[0,0,0,1,0,0],[0,1,0,0,1,0],[1,0,0,1,0,0]]
    options = ['a','b','c']
    for option in options:
        for array in testArrayOfArrays:
            print("option: \'" + option + "\'   " + "array: " + str(array))
            print(checkIfArrayHolds(array, option))

    