# Solver for suduko puzzles
# Author: Jesper Glas

TEST: list[int] = [
        0, 0, 0, 2, 6, 0, 7, 0, 1,
        6, 8, 0, 0, 7, 0, 0, 9, 0,
        1, 9, 0, 0, 0, 4, 5, 0, 0,
        8, 2, 0, 1, 0, 0, 0, 4, 0,
        0, 0, 4, 6, 0, 2, 9, 0, 0,
        0, 5, 0, 0, 0, 3, 0, 2, 8,
        0, 0, 9, 3, 0, 0, 0, 7, 4,
        0, 4, 0, 0, 5, 0, 0, 3, 6,
        7, 0, 3, 0, 1, 8, 0, 0, 0
        ]

INTER: list[int] = [
        0, 2, 0, 6, 0, 8, 0, 0, 0,
        5, 8, 0, 0, 0, 9, 7, 0, 0,
        0, 0, 0, 0, 4, 0, 0, 0, 0,
        3, 7, 0, 0, 0, 0, 5, 0, 0,
        6, 0, 0, 0, 0, 0, 0, 0, 4,
        0, 0, 8, 0, 0, 0, 0, 1, 3,
        0, 0, 0, 0, 2, 0, 0, 0, 0,
        0, 0, 9, 8, 0, 0, 0, 3, 6,
        0, 0, 0, 3, 0, 6, 0, 9, 0
        ]

DIFF: list[int] = [
        0, 2, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 6, 0, 0, 0, 0, 3,
        0, 7, 4, 0, 8, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 3, 0, 0, 2,
        0, 8, 0, 0, 4, 0, 0, 1, 0,
        6, 0, 0, 5, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 1, 0, 7, 8, 0,
        5, 0, 0, 0, 0, 9, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 4, 0
        ]

# 0  1  2    3  4  5    6  7  8
# 9  10 11   12 13 14   15 16 17
# 18 19 20   21 22 23   24 25 26
#
# 27 28 29   30 31 32   33 34 35
# 36 37 38   39 40 41   42 43 44
# 45 46 47   48 49 50   51 52 53
#
# 54 55 56   57 58 59   60 61 62
# 63 64 65   66 67 68   69 70 71
# 72 73 74   75 76 77   78 79 80

def main():
    print(to_string(DIFF))
    print(to_string(solve(DIFF)))


def solve(suduko: list[int]) -> list[int]:
    unmutable: list[bool] = [x > 0 for x in suduko]
    queue: list[int] = []
    index: int = 0
    while index < 81:
        # skip unmutable
        if unmutable[index]:
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
        if i % 27 == 0:
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
