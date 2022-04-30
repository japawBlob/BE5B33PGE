matrix = []
matrix_height = 0


def print_blocks():
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end='')


def add_block(block, block_width, block_height):
    if len(matrix) < 1:
        matrix.append([])
        matrix[matrix_height].append('+')
        for i in range(block_width-1):
            matrix[matrix_height].append('-')
        matrix[matrix_height].append('+')
        matrix.append('\n')
    for i in range(block_height+1):
        for j in range(block_width):
            matrix.append('0')
        matrix.append('\n')

    for i in block:
        print(i)
    print("--------")


if __name__ == '__main__':
    tile_counter = 0
    current_tile = []
    tile_width = 0
    tile_height = 0
    block_width = 0
    block_height = 0
    current_block = []
    max_width = int(input())
    line = []

    while True:
        try:
            line = input().split()
        except EOFError:
            if len(current_tile) > 0:
                if block_width + tile_width + len(current_block) + 1 >= max_width:
                    add_block(current_block, block_width, tile_height)
                    current_block.clear()
                    block_width = 0
                    block_height = 0
                current_block.append(current_tile)
                block_width += tile_width+1
                block_height = max(block_height, tile_height)
                add_block(current_block, block_width, tile_height)
                break
            else:
                if len(current_block) > 0:
                    add_block(current_block, block_width, block_height)
                break
        for i in range(len(line)):
            if len(current_tile) == 0:
                current_tile.append(line[i])
                tile_height += 1
                tile_width = max(tile_width, len(line[i]))
            elif len(line[i]) <= len(current_tile[-1]):
                current_tile.append(line[i])
                tile_height += 1
                tile_width = max(tile_width, len(line[i]))
            else:
                if block_width + tile_width + len(current_block) + 1 >= max_width:
                    add_block(current_block, block_width, tile_height)
                    block_width = 0
                    block_height = 0
                    current_block.clear()
                current_block.append(current_tile.copy())
                block_width += tile_width+1
                block_height = max(block_height, tile_height)
                tile_height = 0
                tile_width = 0
                current_tile.clear()
                current_tile.append(line[i])
                tile_height += 1
                tile_width = max(tile_width, len(line[i]))
    print_blocks()