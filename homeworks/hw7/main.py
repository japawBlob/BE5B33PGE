def print_header_tile(t, w, h):
    var_length = max(len(str(t)), len(str(w)), len(str(h)))
    header_width = 12 + var_length
    ret = ""
    ret += ("+"+"-"*(header_width-2)+"+\n")
    ret += (f"{'| Tile:   ' : <10}{'%d' : >{var_length+(var_length-len(str(t)))}} |\n" % t)
    ret += (f"{'| Width:  ' : <10}{'%d' : >{var_length+(var_length-len(str(w)))}} |\n" % w)
    ret += (f"{'| Height: ' : <10}{'%d' : >{var_length+(var_length-len(str(h)))}} |\n" % h)
    bottom_width = max(header_width, w+2)
    for i in range(bottom_width+1):
        if i == 0 or i == min(header_width-2, w)+1 or i == bottom_width-1:
            ret += "+"
        elif i == bottom_width:
            ret += "\n"
        else:
            ret += "-"
    print(ret, end="")
    return ret


def print_tile(tile_number, tile_body):
    width = max(len(i) for i in tile_body)
    height = len(tile_body)

    print_header_tile(tile_number, width, height)
    for t in range(height-1, -1, -1):
        print("|"+f"{tile_body[t] : >{width}}"+"|")
    print("+"+"-"*width+"+")


if __name__ == '__main__':
    tile_number = 1
    tile_counter = 0
    tile = []
    while True:
        try:
            line = input().split()
        except EOFError:
            if len(tile) > 0:
                print_tile(tile_number, tile)
            exit(0)
        for i in range(0, len(line)):
            if len(tile) == 0:
                tile.append(line[0])
            elif len(line[i]) <= len(tile[tile_counter]):
                tile.append(line[i])
                tile_counter += 1
            else:
                print_tile(tile_number, tile)
                tile.clear()
                tile.append(line[i])
                tile_number += 1
                tile_counter = 0