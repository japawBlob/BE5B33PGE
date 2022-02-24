class simpleGraphicalEditor(object):
    def __init__(self, W, H, N):
        self.W = W
        self.H = H
        self.N = N
        # self.displayMatrix = []

        # for i in range (self.H):
        #     blob = []
        #     for j in range (self.W):
        #         blob.append('.')
        #     self.displayMatrix.append(blob)

        self.displayMatrix = [["." for i in range(W)] for j in range(H)] 


        # self.displayMatrix = [
    def pyramid (self, y1, x1, x2, char):
        while x2-x1 >= 0:
            if( y1 < self.H):
                limX1 = min(max(0, x1), self.W)
                limX2 = min(max(0, x2+1), self.W)
                for x in range (limX1, limX2):
                    self.displayMatrix[y1][x] = char
            # else:
            #     diff = y1-self.H
            #     y1 -= diff
            #     x1 += diff
            #     y1 -= diff
            y1-=1
            if y1 < 0:
                break
            x1+=1
            x2-=1

    def substitute (self, y1, x1, y2, x2, char1, char2):
        for y in range (y1, y2+1):
            for x in range (x1, x2+1):
                if self.displayMatrix[y][x] == char1:
                    self.displayMatrix[y][x] = char2

    def rectangle (self, y1, x1, y2, x2, char):
        for y in range (y1, y2+1):
            for x in range (x1, x2+1):
                self.displayMatrix[y][x] = char

    def clear (self, y1, x1, y2, x2):
        for y in range (y1, y2+1):
            for x in range (x1, x2+1):
                self.displayMatrix[y][x] = '.'

    def readAndExecuteCommands (self):
        for i in range (self.N):
            line = input().split()
            # print(line)
            if line[0] == 'C':
                y1 = min(max(0, int(line[1])), self.H)
                x1 = min(max(0, int(line[2])), self.W)
                y2 = min(max(0, int(line[3])), self.H-1)
                x2 = min(max(0, int(line[4])), self.W-1)
                self.clear(y1, x1, y2, x2)
            if line[0] == 'R':
                y1 = min(max(0, int(line[1])), self.H)
                x1 = min(max(0, int(line[2])), self.W)
                y2 = min(max(0, int(line[3])), self.H-1)
                x2 = min(max(0, int(line[4])), self.W-1)
                self.rectangle(y1, x1, y2, x2, line[5])
            if line[0] == 'S':
                y1 = min(max(0, int(line[1])), self.H)
                x1 = min(max(0, int(line[2])), self.W)
                y2 = min(max(0, int(line[3])), self.H-1)
                x2 = min(max(0, int(line[4])), self.W-1)
                self.substitute(y1, x1, y2, x2, line[5], line[6])
            if line[0] == 'P':
                # y1 = min(max(0, int(line[1])), self.H-1)
                # x1 = min(max(0, int(line[2])), self.W-1)
                # x2 = min(max(0, int(line[3])), self.W-1)
                y1 = int(line[1])
                x1 = int(line[2])
                x2 = int(line[3])
                self.pyramid(y1, x1, x2, line[4])
            # self.printDisplayMatrix()
            # print()

    # def printDisplayMatrix (self):
    #     for i in range (self.H):
    #         for j in range (self.W):
    #             print(self.displayMatrix[i][j], end=" ")
    #         print()

    def printDisplayMatrix (self):
        for i in range (self.H):
            for j in range (self.W):
                print(self.displayMatrix[i][j], end="")
            print()
    

if __name__ == '__main__':
    line = input().split()

    # print(line)

    W = int(line[0])
    H = int(line[1])
    N = int(line[2])
    
    sge = simpleGraphicalEditor(W,H,N)
    sge.readAndExecuteCommands()
    sge.printDisplayMatrix()

    #for i in range(N):
    #    sge.readAndExecuteCommand()