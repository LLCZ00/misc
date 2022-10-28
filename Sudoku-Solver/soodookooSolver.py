# solves sudoku puzzles

"""
dooku = [   # 0          1          2
             [0, 0, 0,   0, 0, 0,   0, 0, 0],  # 0
             [0, 3, 0,   0, 0, 0,   1, 6, 0],  # 1
             [0, 6, 7,   0, 3, 5,   0, 0, 4],  # 2
            # 3          4          5
             [6, 0, 8,   1, 2, 0,   9, 0, 0],  # 3
             [0, 9, 0,   0, 8, 0,   0, 3, 0],  # 4
             [0, 0, 2,   0, 7, 9,   8, 0, 6],  # 5
            # 6          7          8
             [8, 0, 0,   6, 9, 0,   3, 5, 0],  # 6
             [0, 2, 6,   0, 0, 0,   0, 9, 0],  # 7
             [0, 0, 0,   0, 0, 0,   0, 0, 0]   # 8
    ]       # 0  1  2    3  4  5    6  7  8
"""


class Sudoko:
    def __init__(self, sudo):
        self.puzzle = sudo
        self.positions = []

    def get_line(self, line_num):
        return self.puzzle[line_num]

    def get_column(self, column_num):
        column = []
        for number in self.puzzle:
            column.append(number[column_num])
        return column

    def get_square(self, line_group, column_group):  # retrieves "square" based on line and column coordinates
        square = []
        for i in range(line_group[0], line_group[1]):
            for line in self.get_line(i)[column_group[0]:column_group[1]]:
                square.append(line)
        return square

    @staticmethod
    def find_square(line_or_column):  # locates square to be passed to get_square function
        pos = 0
        while True:
            if pos <= line_or_column < pos + 3:
                return pos, pos + 3
            else:
                pos += 3

    def check_sides(self, number, line, column):
        if number not in self.get_line(line):
            if number not in self.get_column(column):
                if number not in self.get_square(self.find_square(line), self.find_square(column)):
                    return True
        return False

    def next_empty(self):
        for line in range(len(self.puzzle)):
            for column in range(len(self.puzzle[line])):
                if self.puzzle[line][column] == 0:
                    return line, column
        return None

    def solve(self):
        coords = self.next_empty()
        if not coords:
            return True
        else:
            line, column = coords

        for number in range(1, 10):
            if self.check_sides(number, line, column):
                self.puzzle[line][column] = number

                if self.solve():
                    return True

                self.puzzle[line][column] = 0

        return False

    def print_puzzle(self):
        for line in self.puzzle:
            print(line)


'''
if __name__ == '__main__':
    puzzle = Sudoko(dooku)
    puzzle.solve()
    puzzle.print_puzzle()
'''


