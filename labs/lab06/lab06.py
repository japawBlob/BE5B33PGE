
# PAG Section D, problem 8

def recu_print_x(number_of_prints):
    if number_of_prints < 1:
        return
    recu_print_x(number_of_prints-1)
    print("x", end="")


def recu_problem_8(leg_size):
    if leg_size < 1:
        return
    recu_problem_8(leg_size-1)
    recu_print_x(leg_size)
    print()


def create_list_of_all_pairs(input_list):
    if len(input_list) <= 1:
        return []
    ret = []
    for i in input_list[1:]:
        ret.append( [input_list[0], i])
    ret.extend(create_list_of_all_pairs(input_list[1:]))
    return ret



if __name__ == '__main__':
    # recu_problem_8(5)
    input_list = [1, 2, 3, 4, 5, 6]
    output_list = []
    ret = create_list_of_all_pairs(input_list)
    for i in ret:
        print(i)
# prints:
# x
# xx
# xxx
# xxxx
# xxxxx
