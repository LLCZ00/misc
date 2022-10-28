# Simple connect 4 game
# This version requires 2 human players

class C4:
    def __init__(self):
        self.board = [
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         ]
        self.lastmove = (0, 0)  # row, column. board[row][column]
        self.lrd = [  # left to right diagonal
            [(2, 0), (3, 1), (4, 2), (5, 3)],
            [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4)],
            [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
            [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6)],
            [(0, 2), (1, 3), (2, 4), (3, 5), (4, 6)],
            [(0, 3), (1, 4), (2, 5), (3, 6)]
        ]
        self.rld = [  # right to left diagonal
            [(0, 3), (1, 2), (2, 1), (3, 0)],
            [(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)],
            [(0, 5), (1, 4), (2, 3), (3, 2), (4, 1), (5, 0)],
            [(0, 6), (1, 5), (2, 4), (3, 3), (4, 2), (5, 1)],
            [(1, 6), (2, 5), (3, 4), (4, 3), (5, 2)],
            [(2, 6), (3, 5), (4, 4), (5, 3)]
        ]

    def print_board(self):
        for row in self.board:
            for cell in row:
                print(cell, end='  ')
            print()

    def move(self, player, column):
        column -= 1
        for b in range(len(self.board)):  # 6
            if self.board[b][column] != 0:
                if b == 0:
                    print("invalid")
                    break
                else:
                    self.board[b - 1][column] = player
                    self.lastmove = (b-1, column)
                    break

            if (b == 5) and (self.board[b][column] == 0):
                self.board[b][column] = player
                self.lastmove = (b, column)
                break

    def check_win(self):  # check horizontal, diagonal, and vertical
        player = self.board[self.lastmove[0]][self.lastmove[1]]
        counter = 0
        flag = 0  # 1 when the previous cell checked is the same as current cell
        for cell in range(7):  # horizonal check
            if counter == 4:
                break
            if self.board[self.lastmove[0]][cell] == player:
                flag = 1
                counter += 1
            else:
                flag = 0
                counter = 0

        for cell in range(6):  # vertical check
            if counter == 4:
                break
            if self.board[cell][self.lastmove[1]] == player:
                flag = 1
                counter += 1
            else:
                flag = 0
                counter = 0

        for chart in self.lrd:
            if self.lastmove in chart:
                for cell in chart:
                    if counter == 4:
                        break
                    if self.board[cell[0]][cell[1]] == player:
                        flag = 1
                        counter += 1
                    else:
                        flag = 0
                        counter = 0

        for chart in self.rld:
            if self.lastmove in chart:
                for cell in chart:
                    if counter == 4:
                        break
                    if self.board[cell[0]][cell[1]] == player:
                        flag = 1
                        counter += 1
                    else:
                        flag = 0
                        counter = 0

        if flag and (counter >= 4):
            return 1
        return 0

    @staticmethod
    def input_check(user_in):
        try:
            i = int(user_in)
        except ValueError:
            return 0
        if (i > 7) or (i < 0):
            return 0

        return 1

    def play(self):
        print("~~~~~~~~~~ Connect Four ~~~~~~~~~~")
        k = input("Press enter to start")
        player = ('r', 'y')
        names = ('Red', 'Yellow')
        x = 0
        while True:  # Red starts first
            self.print_board()
            m = input(f"{names[x]} player: ")
            if self.input_check(m):
                self.move(player[x], int(m))
                if self.check_win():
                    self.print_board()
                    print(f"***** {names[x]} Player Wins *****")
                    break

                if x:
                    x = 0
                else:
                    x = 1
            else:
                print("Invalid column number.")
                continue

        print("Successful exit")


if __name__ == "__main__":
    b = C4()
    b.play()
