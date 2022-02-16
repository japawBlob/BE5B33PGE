def readInputData ():
    firstLine = input().split()
    rows = int(firstLine[0])
    cols = int(firstLine[1])
    matrix = []
    for i in range (rows):
        line = input().split(" ")
        blob = []
        for j in range (cols):
            blob.append(int(line[j]))
        matrix.append(blob)
    return rows,cols,matrix

def printMartix (matrix): 
    for i in range (len(matrix)):
        for j in range (len(matrix[i])):
            print(matrix[i][j], end =" ")
        print()

#potom co zjistím, že jedním směrem je to OK, tak můžu odfajfkovat jako parity OK i všechny následující čísla do len-2

def getParityMatrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    parityMatrix = [["." for i in range(cols)] for j in range(rows)] 

    #for r in range(rows):
    r = 0
    while r < rows:
        #for c in range(cols):
        c = 0
        while c < cols:
            if matrix[r][c] == 'X':
                c += 1
                continue
            if cols - c > 2:
                currentIndex = c+1
                currentParity = matrix[r][currentIndex] % 2
                currentIndex += 1
                fail = False
                while currentIndex < cols:
                    if matrix[r][currentIndex] % 2 != currentParity:
                        fail = True
                    currentIndex += 1
                if fail == False:
                    for i in range (c, cols - 2):
                        parityMatrix[r][i] = 'X'
                    c = cols-2
                    continue

            if rows - r > 2:
                currentIndex = r+1
                currentParity = matrix[currentIndex][c] % 2
                currentIndex += 1
                fail = False
                while currentIndex < rows:
                    if matrix[currentIndex][c] % 2 != currentParity:
                        fail = True
                    currentIndex += 1
                if fail == False:
                    for i in range (r, rows - 2):
                        parityMatrix[i][c] = 'X'
                    #r = rows-2
                    c += 1
                    continue

            if c >= 2:
                currentIndex = c-1
                currentParity = matrix[r][currentIndex] % 2
                currentIndex -= 1
                fail = False
                while currentIndex >= 0:
                    if matrix[r][currentIndex] % 2 != currentParity:
                        fail = True
                    currentIndex -= 1
                if fail == False:
                    #for i in range (c, cols - 2):
                    #    parityMatrix[r][i] = 'X'
                    # c = cols-2
                    parityMatrix[r][c] = 'X'
                    c += 1
                    continue


            

            if r >= 2:
                currentIndex = r-1
                currentParity = matrix[currentIndex][c] % 2
                currentIndex -= 1
                fail = False
                while currentIndex >= 0:
                    if matrix[currentIndex][c] % 2 != currentParity:
                        fail = True
                    currentIndex -= 1
                if fail == False:
                    #for i in range (c, cols - 2):
                    #    parityMatrix[r][i] = 'X'
                    #c = cols-2
                    parityMatrix[r][c] = 'X'
                    c += 1
                    continue
            c += 1
        r += 1

    printMartix(parityMatrix)

def getParityMatrix2 (matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    parityMatrix = [["." for i in range(cols)] for j in range(rows)] 

    for r in range(rows):
        if matrix[r][0] % 2 == matrix[r][1] % 2:
            parity = matrix[r][0] % 2
            parityMatrix[r][2] = 'X'
            for c in range(3, cols):
                if matrix[r][c-1] % 2 == parity:
                    parityMatrix[r][c] = 'X'
                else:
                    break

    for r in range(rows):
        if matrix[r][cols-1] % 2 == matrix[r][cols-2] % 2:
            parity = matrix[r][cols-1] % 2
            parityMatrix[r][cols-3] = 'X'
            for c in range(3, cols):
                if matrix[r][cols-c] % 2 == parity:
                    parityMatrix[r][cols-c-1] = 'X'
                else:
                    break

    for c in range(cols):
        if matrix[0][c] % 2 == matrix[1][c] % 2:
            parity = matrix[0][c] % 2
            parityMatrix[2][c] = 'X'
            for r in range(3, rows):
                if matrix[r-1][c] % 2 == parity:
                    parityMatrix[r][c] = 'X'
                else:
                    break

    for c in range(cols):
        if matrix[rows-1][c] % 2 == matrix[rows-2][c] % 2:
            parity = matrix[rows-1][c] % 2
            parityMatrix[rows-3][c] = 'X'
            for r in range(3, rows):
                if matrix[rows-r][c] % 2 == parity:
                    parityMatrix[rows-r-1][c] = 'X'
                else:
                    break

    printMartix(parityMatrix)


if __name__ == '__main__':
    rows,cols,matrix = readInputData()

    # printMartix(matrix)

    # print(str(rows) + " " + str(cols))

    getParityMatrix2(matrix)