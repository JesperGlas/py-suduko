# Solver for suduko puzzles
# Author: Jesper Glas

import sys


def main():
    # make sure call has an argument (the suduko)
    if len(args := sys.argv) < 2:
        print("Please provide a suduko in the form '020 045 100...' where 0 represents empty spaces.")
        return 1

    # make sure that input is of correct length
    if len(suduko := format_input(args[1])) != 81:
        print(len(suduko))
        print("Please provide a suduko with exactly 81 values.")
        return 1

    # print results
    print(f"Original:\n{to_string(suduko)}")
    print('\n')
    print(f"Solved:\n{to_string(solve(suduko))}")

def format_input(raw: str) -> list[int]:
    # remove leading spaces
    data: str = raw.strip()
    # remove all whitespace
    data = data.replace(' ', '')
    # remove newlines
    data = data.replace('\n', '')
    return [int(char) for char in data]


def solve(suduko: list[int]) -> list[int]:
    # keeps track of immutable values (original suduko entries)
    immutable: list[bool] = [x > 0 for x in suduko]
    # variables for DFS, using list (suduko) index
    queue: list[int] = []
    index: int = 0
    # end condition of loop is last element
    while index < 81:
        # skip immutable
        if immutable[index]:
            index += 1
            continue

        # variables needed for action to continue
        val: int = suduko[index]
        opt: list[int] = [x for x in get_options(index, suduko) if x > val]

        # if there are available options
        if len(opt) > 0:
            suduko[index] = opt[0]
            queue.append(index)
            index += 1
            continue
        
        # check if queue is populated, else its unsolvable
        if len(queue) == 0:
            break

        # else, backtrack in queue
        suduko[index] = 0
        index = queue.pop()

    return suduko

def get_elem_row(index: int, suduko: list[int]) -> set[int]:
    start: int = index - (index % 9)
    return set([suduko[n] for n in range(start, start+9)])

def get_elem_col(index: int, suduko: list[int]) -> set[int]:
    start: int = index % 9
    return set([suduko[n] for n in range(start, 81, 9)])

def get_elem_quad(index: int, suduko: list[int]) -> set[int]:
    res: set[int] = set()
    row: int = index // 27
    col: int = index // 3 % 3
    i: int = row * 27 + col * 3
    for n in range(0, 3):
        for m in range(0, 3):
            res.add(suduko[i])
            i += 1
        i += 6
    return res

def get_options(index: int, suduko: list[int]) -> list[int]:
    non_valid: set[int] = set()
    current: int = suduko[index]
    non_valid.update(get_elem_row(index, suduko))
    non_valid.update(get_elem_col(index, suduko))
    non_valid.update(get_elem_quad(index, suduko))
    non_valid = set(range(1, 10)).difference(non_valid)
    return sorted(non_valid)

def to_string(data: list[int]) -> str:
    res: str = ""
    for i, x in enumerate(data):
        # add additional newline every third row
        if i % 27 == 0 and i != 0:
            res += "\n\n"
        # add standard new line every ninth element
        elif i % 9 == 0:
            res += '\n'
        # add addional spaces every third column
        elif i % 3 == 0:
            res += "  "

        res += f" {x}"

    return res


if __name__ == "__main__":
    main()
