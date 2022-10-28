import cv2
import pytesseract as pt
import soodookooSolver as ss

# initialize pytesseract (pulls text from images)
pt.pytesseract.tesseract_cmd = 'C:{your files}/tesseract.exe'  # location of tesseract.exe


def find_squares(puzzle):  # finds the squares in the image and isolates them in a list
    squares_list = []
    gray = cv2.cvtColor(puzzle, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]  # 200

    cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            squares_list.append(puzzle.copy()[y:y + h, x:x + w])
    return squares_list


def read_numbers(square_images):
    number_list = []
    for image in square_images:
        number = pt.image_to_string(image, config='--psm 6')  # psm 6 allows single digits to be read. somehow.
        if number:
            if number == 'A':
                number_list.append(4)
            else:
                number_list.append(int(number))
        else:
            number_list.append(0)
    return number_list


def sudoko_format(num_list):  # puts numbers into a format that soodookooSolver.py understands
    puzzle_format = [[], [], [], [], [], [], [], [], []]
    shift = 0
    for line in puzzle_format:
        for number in range(9):
            line.append(num_list[number + shift])
        shift += 9
    return puzzle_format


def solve(puzzle_list):
    puzzle = ss.Sudoko(puzzle_list)
    puzzle.solve()
    return puzzle.puzzle


def main():
    img = cv2.imread("assets/sudoku_img.png")
    squares = find_squares(img)[::-1]
    number_list = read_numbers(squares)  # takes the most time
    puzzle = sudoko_format(number_list)
    solved = solve(puzzle)

    for line in solved:
        print(line)


if __name__ == '__main__':
    main()
