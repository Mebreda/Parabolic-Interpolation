from tkinter import *
from tkinter import ttk, simpledialog, messagebox
from functools import partial
from main import *

"""
Generates initial guesses entries
"""


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

    return text_var, entries


"""
Generates the equation frame
"""


def generate_equation_frame(frame):
    text = Label(frame, text="f(x) = ")
    text.grid(row=0, column=0)
    text_var = StringVar()
    equation_box = Entry(frame, textvariable=text_var, width=60)
    equation_box.grid(row=0, column=1)
    text2 = Label(frame, text="ex. 4*x-1.8*x^2+1.2*x^3-0.3*x^4")
    text2.grid(row=1, column=1)
    text3 = Label(frame, text="2*sin(x)-(x^2/10)")
    text3.grid(row=2, column=1)
    return equation_box, text_var


"""
Generates the table
"""


def generate_table(frame):
    diagonal_matrix_box = Text(frame, height=30, width=100)
    diagonal_matrix_box.grid(row=0, column=0)
    scrollbar = ttk.Scrollbar(frame, command=diagonal_matrix_box.yview)
    scrollbar.grid(row=0, column=1, sticky='nsew')
    diagonal_matrix_box['yscrollcommand'] = scrollbar.set


"""
Generates the solution
"""


def generate_solution(frame):
    sol_frm = ttk.Frame(frame, padding="12 10 12 12")
    deriv_frm = ttk.LabelFrame(frame, padding="10 0 10 10")
    sol_box = Text(sol_frm, height=4, width=30)
    deriv_btn = ttk.Button(deriv_frm, text="Show Solution", command=partial(show_derivation, frame))
    sol_box.grid(row=0, column=0)
    deriv_btn.grid(row=10, column=0)

    sol_frm.grid(row=0, column=0)
    deriv_frm.grid(row=1, column=0)


"""
Generates the controls
"""


def generate_controls(frame, text_var, entries_vars, eq_text_var, eq_entry_var, right_frame):
    solvebtn = ttk.Button(frame, text="Solve", command=partial(solve_handler, text_var, eq_text_var, right_frame))
    solvebtn.grid(row=0, column=0)
    clearbtn = ttk.Button(frame, text="Clear", command=partial(clear_fields, entries_vars, eq_entry_var))
    clearbtn.grid(row=0, column=1)


"""
Restarts the program if the problem has been solved 
"""


def check_problem():
    if my_result.getvalue() != '':
        messagebox.showinfo("Information", "Operation Complete")
        messagebox.showinfo("Information", "Restarting Program")
        os.execl(sys.executable, sys.executable, *sys.argv)


"""
Clears the fields
"""


def clear_fields(entries_vars, eq_entry_var):
    blank = ""
    for row in range(len(entries_vars)):
        entries_vars[row].delete(0, END)

    check_problem()
    eq_entry_var.delete(0, END)
    update_right_subframe(right_frame.children['!labelframe'], blank)
    update_sol_subframe(right_frame.children['!labelframe2'].children['!frame'], blank, blank)


"""
Uses the functions in main.py to solve the problem
Updates the tables and solutions
"""


def solve_handler(text_var, eq_text_var, right_frame):
    check_problem()

    try:
        x0 = float(text_var[0].get())
        x1 = float(text_var[1].get())
        x2 = float(text_var[2].get())
        equation = eq_text_var.get()
        x3, f3, table = parabolic_interpolation(x0, x1, x2, equation)
    except ValueError:
        messagebox.showerror("Error", "Invalid input")

    update_right_subframe(right_frame.children['!labelframe'], table)
    update_sol_subframe(right_frame.children['!labelframe2'].children['!frame'], x3, f3)


"""
Updates the right subframe
"""


def update_right_subframe(frame, mat):
    frame.children['!text'].delete('1.0', 'end')
    frame.children['!text'].insert('1.0', str(mat))


"""
Updates the solution subframe
"""


def update_sol_subframe(frame, x3, f3):
    frame_str = ""
    if x3 and f3 != "":
        frame_str = "x = " + str(x3)
        frame_str = frame_str + '\n'
        frame_str = frame_str + "True value = " + str(f3)

    if x3 or f3 == 0:
        frame_str = "x = " + str(x3)
        frame_str = frame_str + '\n'
        frame_str = frame_str + "True value = " + str(f3)

    frame.children['!text'].delete('1.0', 'end')
    frame.children['!text'].insert('1.0', frame_str)


"""
Shows the derivation
"""


def show_derivation(root):
    window = Toplevel(root)

    s = my_result.getvalue()

    window_frame = ttk.Frame(window, padding="12 10 12 12")
    window_frame.grid(row=0, column=0)

    deriv_box = Text(window_frame, height=25, width=120)
    deriv_box.grid(row=0, column=0)

    # Scrollbar logic
    scrollbar = ttk.Scrollbar(window_frame, command=deriv_box.yview)
    scrollbar.grid(row=0, column=1, sticky='nsew')
    deriv_box['yscrollcommand'] = scrollbar.set
    deriv_box.delete('1.0', 'end')
    deriv_box.insert('1.0', s)

    window.title("Derivation Window")
    # Label(window, text=s, font=('Mistral 18 bold')).place(x=150, y=80)

"""
Main Class
"""
if __name__ == '__main__':
    # Create the root frame
    root = Tk()
    root.title("Parabolic Interpolation Utility")
    # Create the content frame (main frame)
    main_frame = ttk.Frame(root, padding="12 12 12 12")
    # Standard practice, a top level frame must hold other components
    main_frame.grid(column=0, row=0, sticky=(N, W, E, S))
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

    right_frame = ttk.LabelFrame(main_frame, padding="12 12 12 12")
    right_frame.grid(row=0, column=1)

    generate_controls(control_frame, text_vars, entries_vars, eq_text_var, eq_entry_var, right_frame)

    # Populate the right frame
    # Table Frame
    table_frame = ttk.LabelFrame(right_frame, padding="12 10 12 12", text="Table")
    table_frame.grid(row=0, column=0)
    generate_table(table_frame)

    # Solution to the problem
    solution = ttk.LabelFrame(right_frame, padding="12 10 12 12", text="Solution to the system")
    solution.grid(row=1, column=0)
    generate_solution(solution)

    root.mainloop()
