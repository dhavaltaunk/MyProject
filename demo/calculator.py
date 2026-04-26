import tkinter as tk
from tkinter import font

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("330x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#1f1f2e")

        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (1, 0), 8: (1, 1), 9: (1, 2),
            4: (2, 0), 5: (2, 1), 6: (2, 2),
            1: (3, 0), 2: (3, 1), 3: (3, 2),
            0: (4, 0), ".": (4, 1)
        }
        self.operations = { "/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+" }

        self.button_frame = self.create_button_frame()
        self.button_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.button_frame.rowconfigure(x, weight=1)
            self.button_frame.columnconfigure(x - 1, weight=1)

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

        self.update_label()
        self.update_total_label()

    def bind_keys(self):
        self.root.bind("<Return>", lambda event: self.evaluate())
        self.root.bind("<BackSpace>", lambda event: self.clear_last())
        for key in self.digits:
            self.root.bind(str(key), lambda event, digit=key: self.add_to_expression(str(digit)))
        self.root.bind(".", lambda event: self.add_to_expression("."))
        for key in self.operations:
            self.root.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_display_labels(self):
        total_label = tk.Label(
            self.display_frame,
            text=self.total_expression,
            anchor=tk.E,
            bg="#1f1f2e",
            fg="#7c7c8a",
            padx=24,
            font=("Segoe UI", 16)
        )
        total_label.pack(expand=True, fill="both")

        label = tk.Label(
            self.display_frame,
            text=self.current_expression or "0",
            anchor=tk.E,
            bg="#1f1f2e",
            fg="#ffffff",
            padx=24,
            font=("Segoe UI", 40, "bold")
        )
        label.pack(expand=True, fill="both")

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.root, height=160, bg="#1f1f2e")
        frame.pack(expand=True, fill="both")
        return frame

    def create_button_frame(self):
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill="both")
        return frame

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(
                self.button_frame,
                text=str(digit),
                bg="#2e2e44",
                fg="white",
                font=("Segoe UI", 24, "bold"),
                borderwidth=0,
                command=lambda x=digit: self.add_to_expression(str(x))
            )
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW, padx=1, pady=1)

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(
                self.button_frame,
                text=symbol,
                bg="#ff9500",
                fg="white",
                font=("Segoe UI", 24, "bold"),
                borderwidth=0,
                command=lambda x=operator: self.append_operator(x)
            )
            button.grid(row=i, column=3, sticky=tk.NSEW, padx=1, pady=1)
            i += 1

    def create_special_buttons(self):
        clear_button = tk.Button(
            self.button_frame,
            text="C",
            bg="#ff3b30",
            fg="white",
            font=("Segoe UI", 24, "bold"),
            borderwidth=0,
            command=self.clear
        )
        clear_button.grid(row=0, column=0, sticky=tk.NSEW, padx=1, pady=1)

        delete_button = tk.Button(
            self.button_frame,
            text="⌫",
            bg="#5e5e7a",
            fg="white",
            font=("Segoe UI", 24, "bold"),
            borderwidth=0,
            command=self.clear_last
        )
        delete_button.grid(row=0, column=1, sticky=tk.NSEW, padx=1, pady=1)

        percent_button = tk.Button(
            self.button_frame,
            text="%",
            bg="#5e5e7a",
            fg="white",
            font=("Segoe UI", 24, "bold"),
            borderwidth=0,
            command=lambda: self.append_operator("%")
        )
        percent_button.grid(row=0, column=2, sticky=tk.NSEW, padx=1, pady=1)

        equals_button = tk.Button(
            self.button_frame,
            text="=",
            bg="#007aff",
            fg="white",
            font=("Segoe UI", 24, "bold"),
            borderwidth=0,
            command=self.evaluate
        )
        equals_button.grid(row=4, column=2, columnspan=2, sticky=tk.NSEW, padx=1, pady=1)

        zero_button = tk.Button(
            self.button_frame,
            text="0",
            bg="#2e2e44",
            fg="white",
            font=("Segoe UI", 24, "bold"),
            borderwidth=0,
            command=lambda: self.add_to_expression("0")
        )
        zero_button.grid(row=4, column=0, columnspan=1, sticky=tk.NSEW, padx=1, pady=1)

        dot_button = tk.Button(
            self.button_frame,
            text=".",
            bg="#2e2e44",
            fg="white",
            font=("Segoe UI", 24, "bold"),
            borderwidth=0,
            command=lambda: self.add_to_expression(".")
        )
        dot_button.grid(row=4, column=1, sticky=tk.NSEW, padx=1, pady=1)

    def add_to_expression(self, value):
        if value == "." and "." in self.current_expression:
            return
        self.current_expression += value
        self.update_label()

    def append_operator(self, operator):
        if self.current_expression == "" and self.total_expression == "":
            return
        if self.current_expression == "" and self.total_expression:
            self.total_expression = self.total_expression[:-1] + operator
        else:
            self.total_expression += self.current_expression + operator
            self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def clear_last(self):
        self.current_expression = self.current_expression[:-1]
        self.update_label()

    def evaluate(self):
        if not self.current_expression and not self.total_expression:
            return
        expression = self.total_expression + self.current_expression
        expression = expression.replace("\u00F7", "/").replace("\u00D7", "*")
        try:
            result = str(eval(expression))
            self.current_expression = result
            self.total_expression = ""
        except Exception:
            self.current_expression = "Error"
        self.update_label()
        self.update_total_label()

    def update_total_label(self):
        self.total_label.config(text=self.total_expression)

    def update_label(self):
        self.label.config(text=self.current_expression or "0")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()