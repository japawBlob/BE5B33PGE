def readInputData ():
    #x = int(input()) 
    #y = int(input())

    x,y = int(input().split())

    matrix = [x][y]

    for i in range (x):
        for j in range (y):
            matrix[i][j] = int(input())

    return x,y,matrix



if __name__ == '__main__':
    x,y,matrix = readInputData()

    print(x + " " + y)