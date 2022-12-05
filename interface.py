from tkinter import *
from tkinter import ttk, simpledialog
from functools import partial
from main import *


def generate_initial_guess_entries(frame):
    text_var = []
    entries = []
    x0 = Label(frame, text="x0 = ")
    x1 = Label(frame, text="x1 = ")
    x2 = Label(frame, text="x2 = ")
    x0.grid(row=0, column=0)
    x1.grid(row=1, column=0)
    x2.grid(row=2, column=0)

    for ctr in range(3):
        text_var.append(StringVar())
        entries.append(Entry(frame, textvariable=text_var[ctr], width=6))
        entries[ctr].grid(row=ctr, column=1)

    # for row in range(rows):
    #     # temporary 1D array for the 2D array (matrix)
    #     text_var.append([])
    #     entries.append([])
    #     for col in range(cols):
    #         text_var[row].append(StringVar())
    #         entries[row].append(Entry(frame, textvariable=text_var[row][col], width=6))
    #         entries[row][col].grid(row=row, column=col)
    return text_var, entries


def generate_equation_frame(frame):
    text = Label(frame, text="f(x) = ")
    text.grid(row=0, column=0)
    text_var = StringVar()
    equation_box = Entry(frame, textvariable=text_var, width=60)
    equation_box.grid(row=0, column=1)
    return equation_box, text_var


def generate_table(frame):
    diagonal_matrix_box = Text(frame, height=30, width=90)
    diagonal_matrix_box.grid(row=0, column=0)


def generate_solution(frame):
    sol_frm = ttk.Frame(frame, padding="12 10 12 12")
    deriv_frm = ttk.LabelFrame(frame, padding="10 0 10 10")
    sol_box = Text(sol_frm, height=4, width=30)
    deriv_btn = ttk.Button(deriv_frm, text="Show Derivation", command=partial(show_derivation, frame))
    sol_box.grid(row=0, column=0)
    deriv_btn.grid(row=10, column=0)

    sol_frm.grid(row=0, column=0)
    deriv_frm.grid(row=1, column=0)


def generate_controls(frame, text_var, entries_vars, eq_text_var, eq_entry_var, right_frame):
    # text_var, eqn_widget, A, B, X
    solvebtn = ttk.Button(frame, text="Solve",
                          command=partial(solve_handler, text_var, eq_text_var, right_frame))
    solvebtn.grid(row=0, column=0)
    clearbtn = ttk.Button(frame, text="Clear", command=partial(clear_fields, entries_vars, eq_entry_var))
    clearbtn.grid(row=0, column=1)


# def extract_matrix_input(text_var):
    # Create a matrix of N X (N + 1), where the 1 increment
    # is allocated for the RHS (matrix B)
    # coef_arr = np.zeros((len(text_var), (len(text_var) + 1)), dtype=float)
    # for row in range(len(text_var)):
    #     # Represents 1 row in a 2D array
    #     tempArr = []
    #     for col in range(len(text_var[0])):
    #         tempArr.append(float(text_var[row][col].get()))
    #     coef_arr[row] = tempArr.copy()
    #     # Exclude the RHS
    #     A[row] = tempArr.copy()[:len(tempArr) - 1]
    #     B.append(float(tempArr[len(tempArr) - 1]))
    # # Generate X Matrix
    # sub = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    # for i in range(len(text_var)):
    #     X.append(('x' + str(i + 1)).translate(sub))


def show_system(eqn_widget, A, B, X):
    sys_eqn_str = ""
    operand = ""
    for row_index, row in enumerate(A):
        for element_index, element in enumerate(row):
            temp_str = str(abs(element)) + X[element_index]
            if element_index + 1 != len(row):
                next = A[row_index][element_index + 1]
                if next > 0:
                    operand = " + "
                    temp_str += operand
                elif next < 0:
                    operand = " - "
                    temp_str += operand
            sys_eqn_str += temp_str
        sys_eqn_str += (" = " + str(B[row_index]) + '\n')
    eqn_widget.delete('1.0', 'end')
    eqn_widget.insert('1.0', sys_eqn_str)


def clear_mat(mat):
    for row_index, row in enumerate(mat):
        for e_index, e in enumerate(row):
            mat[row_index][e_index] = 0


def clear_arr(arr):
    for i, e in enumerate(arr):
        if isinstance(e, str):
            arr[i] = 0
        else:
            arr[i] = 0


def clear_fields(entries_vars, eq_entry_var):
    blank = ""

    for row in range(len(entries_vars)):
        entries_vars[row].delete(0, END)

    eq_entry_var.delete(0, END)
    update_right_subframe(right_frame.children['!labelframe'], blank)
    update_sol_subframe(right_frame.children['!labelframe2'].children['!frame'], blank, blank)


def solve_handler(text_var, eq_text_var, right_frame):
    # extract_matrix_input(text_var, A, B, X)
    #
    # show_system(eqn_widget, A, B, X)
    x0 = int(text_var[0].get())
    x1 = int(text_var[1].get())
    x2 = int(text_var[2].get())
    equation = eq_text_var.get()
    x3, f3 = parabolic_interpolation(x0, x1, x2, equation)
    s = my_result.getvalue()

    update_right_subframe(right_frame.children['!labelframe'], s)
    update_sol_subframe(right_frame.children['!labelframe2'].children['!frame'], x3, f3)


def update_right_subframe(frame, mat):
    frame.children['!text'].delete('1.0', 'end')
    frame.children['!text'].insert('1.0', str(mat))


def update_d_subframe(frame, D):
    frame_str = ""
    tr_table = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    substr = []
    for i in range(len(D)):
        substr.append(('d' + str(i + 1)).translate(tr_table))

    for i, d in enumerate(D):
        frame_str += substr[i] + " = " + str(d) + '\n'

    frame.children['!text'].delete('1.0', 'end')
    frame.children['!text'].insert('1.0', frame_str)


def update_sol_subframe(frame, x3, f3):
    frame_str = ""
    if x3 and f3 != "":
        frame_str = "x = " + str(x3)
        frame_str = frame_str + '\n'
        frame_str = frame_str + "True value = " + str(f3)

    frame.children['!text'].delete('1.0', 'end')
    frame.children['!text'].insert('1.0', frame_str)


def show_derivation(root):
    window = Toplevel(root)
    s = show_derivation()

    window_frame = ttk.Frame(window, padding="12 10 12 12")
    window_frame.grid(row=0, column=0)

    deriv_box = Text(window_frame, height=16, width=80)
    deriv_box.grid(row=0, column=0)

    # Scrollbar logic
    scrollbar = ttk.Scrollbar(window_frame, command=deriv_box.yview)
    scrollbar.grid(row=0, column=1, sticky='nsew')
    deriv_box['yscrollcommand'] = scrollbar.set
    deriv_box.delete('1.0', 'end')
    deriv_box.insert('1.0', s)

    window.title("Derivation Window")
    # Label(window, text=s, font=('Mistral 18 bold')).place(x=150, y=80)


if __name__ == '__main__':
    # Create the root frame
    root = Tk()
    root.title("Parabolic Interpolation Utility")

    # Create the content frame (main frame)
    main_frame = ttk.Frame(root, padding="12 12 12 12")
    # Standard practice, a top level frame must hold other components
    main_frame.grid(column=0, row=0, sticky=(N, W, E, S))
    # Hold the matrix input fields and the text field that shows
    # the inputted equation
    left_frame = ttk.LabelFrame(main_frame, padding="12 10 12 12")
    left_frame.grid(row=0, column=0)
    # Populate the left frame
    equation_frame = ttk.LabelFrame(left_frame, padding="12 10 12 12", text="Equation")
    initial_guess = ttk.LabelFrame(left_frame, padding="12 10 12 12", text="Initial Guesses")
    control_frame = ttk.LabelFrame(left_frame, padding="12 10 12 12", text="Controls")

    equation_frame.grid(row=1, column=0)
    initial_guess.grid(row=2, column=0)
    control_frame.grid(row=3, column=0)

    text_vars, entries_vars = generate_initial_guess_entries(initial_guess)
    eq_entry_var, eq_text_var = generate_equation_frame(equation_frame)

    # Right frame will contain the L, U and the solutions to the equation
    right_frame = ttk.LabelFrame(main_frame, padding="12 12 12 12")
    right_frame.grid(row=0, column=1)

    generate_controls(control_frame, text_vars, entries_vars, eq_text_var, eq_entry_var, right_frame)

    # Populate the right frame
    # Upper Diagonal Frame
    table_frame = ttk.LabelFrame(right_frame, padding="12 10 12 12", text="Table")
    table_frame.grid(row=0, column=0)
    generate_table(table_frame)

    # Solution to the problem
    solution = ttk.LabelFrame(right_frame, padding="12 10 12 12", text="Solution to the system")
    solution.grid(row=1, column=0)
    generate_solution(solution)

    root.mainloop()
