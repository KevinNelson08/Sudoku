import numpy as np
from dokusan import generators
from tkinter import Button, Entry, Frame, Label, messagebox, StringVar, Tk

# this methods makes the default hints, solves the puzzle and returns the hints and the solution


def hints_solution(difficulty):
    """
    This makes a 9 x 9 grid
    generator makes class object of numbers
    str converts object to str
    list puts str into array
    np.char.replace replaces 0s with empty strings in array
    np reshape convests single array into 9x9 double array
    """
    hints = np.reshape(np.char.replace(
        list(str(generators.random_sudoku(avg_rank=difficulty))), "0", ""), (9, 9))
    # while stats.rank(sudoku := generators.random_sudoku(avg_rank)) < avg_rank:
    # continue
    solution = np.array(hints)
    solve(solution, 0, 0)
    return hints, solution


# When making the solution, this method ensures that numbers do not violate the sukou rules
def rules(grid, row, col, value):
    for x in range(9):
        if grid[row][x] == value or grid[x][col] == value:
            return False
    block_row = row - row % 3
    block_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + block_row][j + block_col] == value:
                return False
    return True


# solves the puzzle given any board
def solve(grid, row, col):
    values = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    if row == 8 and col == 9:
        return True
    if col == 9:
        row += 1
        col = 0
    if grid[row][col] != "":
        return solve(grid, row, col + 1)
    for val in values:
        if rules(grid, row, col, val):
            grid[row][col] = val
            if solve(grid, row, col + 1):
                return True
        grid[row][col] = ""
    return False


# makes a window class odject
class window:
    def __init__(self, title):
        self.window = Tk()
        self.window.title(title)
        self.switch = True
        self.main_page()
        self.window.mainloop()

    # main page of the window
    def main_page(self):
        self.main_widgets = Frame(self.window)
        self.main_widgets.pack()

        self.name = Label(self.main_widgets, text="Sudoku",
                          font="normal 12 bold")
        self.name.pack(padx=10, pady=5)

        self.play = Button(self.main_widgets, text="Play",
                           command=lambda: self.switch_page(100))
        self.play.pack(padx=5, pady=5)

        self.quit_button = Button(
            self.main_widgets, text="Exit", command=quit)
        self.quit_button.pack(padx=5, pady=5)

    # the sudoko game page
    def game_page(self, difficulty):
        # this checks if user puzzle is right
        def check():
            widget_get = []
            for x in range(9):
                row = []
                for y in range(9):
                    col = self.grid[x][y].get()
                    row.append(col)
                widget_get.append(row)
            if (bool(np.asarray(widget_get == solution).all())):
                messagebox.showinfo("", "Congratulations! YOU WON!")
                self.switch_page(None)
            else:
                messagebox.showinfo("", "Oops! You made a mistake")

        # shows or hides the answer sheet
        def show_answers():
            if self.hide_answers:
                self.hide_answers = False
                if (messagebox.askyesno("Show Answer Key", "Are you sure you want to see the answers?")):
                    self.answers.grid(row=1, column=1, padx=20, pady=20)
            else:
                self.hide_answers = True
                self.answers.grid_remove()

        # switches between main page and game page
        def quit():
            if (messagebox.askokcancel("Quiting", "Are You Sure?")):
                self.switch_page(None)

        # ensures user inputs valid option
        def validate(input):
            valid_inputs = ["1", "2", "3", "4", "5", "6", "7", "8", "9", ""]
            if input in valid_inputs:
                return True
            else:
                self.game_widgets.bell()
                return False

        # frame for game page
        self.game_widgets = Frame(self.window)
        self.game_widgets.pack()

        # heading frame
        self.heading = Frame(self.game_widgets)
        self.heading.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # instructions for game
        self.instructions = Label(
            self.heading, text="Enter all the correct number in the right place and you will win!")
        self.instructions.pack()

        # frame for the user board
        # also creates outside block's border, the inside border is in entry widget
        self.board = Frame(self.game_widgets, bg="black", border="2")
        self.board.grid(row=1, column=0, padx=15, pady=15)

        # grabs the hints for the board, and solution for checking
        hints, solution = hints_solution(difficulty)

        # sets validaing user input to the game board
        self.input = (self.game_widgets.register(validate), "%P")

        # makes the user board
        self.grid = []
        for x in range(9):
            row = []
            for y in range(9):
                self.col = Entry(
                    self.board, validate="key", validatecommand=self.input,
                    highlightthickness=1, highlightcolor="green",
                    width=2, justify="center", font="normal 12 bold",
                    insertontime=0)
                row.append(self.col)
                # creates nside block's border, the outer border is in frame
                if x in (3, 6) and y in (2, 5):
                    self.col.grid(row=x, column=y, padx=(
                        0, 2), pady=(2, 0), sticky="nsew")
                elif x in (3, 6):
                    self.col.grid(row=x, column=y, pady=(2, 0), sticky="nsew")
                elif y in (2, 5):
                    self.col.grid(row=x, column=y, padx=(0, 2), sticky="nsew")
                else:
                    self.col.grid(row=x, column=y)
                if hints[x][y]:
                    self.col.insert(0, hints[x][y])
                    self.col.config(state="disabled")
            self.grid.append(row)

        # frame for the solution
        # also creates outside block's border for solution, the inside border is in entry widget
        self.answers = Frame(self.game_widgets, bg="black", border=2)

        self.hide_answers = True

        # creating the solution board
        for x in range(9):
            for y in range(9):
                self.answer = StringVar(self.answers, value=solution[x][y])
                self.col = Entry(
                    self.answers, textvariable=self.answer, state="disabled",
                    highlightthickness=1, width=2, justify="center", font="normal 12 bold")
                # Inside block's border, outer border is in frame
                if x in (3, 6) and y in (2, 5):
                    self.col.grid(row=x, column=y, padx=(
                        0, 2), pady=(2, 0), sticky="nsew")
                elif x in (3, 6):
                    self.col.grid(row=x, column=y, pady=(2, 0), sticky="nsew")
                elif y in (2, 5):
                    self.col.grid(row=x, column=y, padx=(0, 2), sticky="nsew")
                else:
                    self.col.grid(row=x, column=y)

        # frame for the features like show/hide solution, check, and quitting puzzle
        self.features = Frame(self.game_widgets)
        self.features.grid(row=2, column=0, columnspan=2)

        # buttom to compare user board and solution
        self.check_board = Button(
            self.features, text="Check", command=lambda: check())
        self.check_board.grid(row=0, column=0, padx=10, pady=10)

        # buttom for showing/hiding answer board
        self.answer_key = Button(
            self.features, text="Show/Hide Answer Key", command=lambda: show_answers())
        self.answer_key.grid(row=0, column=1, padx=10, pady=10)

        # buttom for going back to main page
        self.quit_game = Button(
            self.features, text="Quit Puzzle", command=lambda: quit())
        self.quit_game.grid(row=0, column=3, padx=10, pady=10)

    # method to switch between main page and game page
    def switch_page(self, difficulty):
        if self.switch:
            self.switch = False
            self.main_widgets.pack_forget()
            self.game_page(difficulty)
        else:
            self.switch = True
            self.game_widgets.pack_forget()
            self.main_page()


if __name__ == "__main__":
    sudoko = window("Sudoko")
