import tkinter as tk
from datetime import datetime
import csv

# Logger class for handling log entries to a CSV file
class KeypressLogger:
    def __init__(self, username, test_case_number):
        # Define the filename with the current date and time
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = f"log_{username}_{test_case_number}_{date_str}.csv"
        # Initialize the file with headers
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Keypress'])

    def log_keypress(self, key):
        # Get the current time with millisecond accuracy
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        # Write the log entry to the CSV file
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, key])

# RPN Calculator logic
class RPNCalculator:
    def __init__(self):
        self.stack = []
        self.current_input = ""

    def press(self, key):
        if key.isdigit():
            self.current_input += key
        elif key in ['+', '-', 'x', '/']:
            if self.current_input:
                self.stack.append(int(self.current_input))
                self.current_input = ""
            if len(self.stack) >= 2:
                self.operate(key)
        elif key == 'Enter':
            if self.current_input:
                self.stack.append(int(self.current_input))
                self.current_input = ""
        elif key == 'C':
            self.stack = []
            self.current_input = ""

    def operate(self, operator):
        b = self.stack.pop()
        a = self.stack.pop()

        if operator == '+':
            result = a + b
        elif operator == '-':
            result = a - b
        elif operator == 'x':
            result = a * b
        elif operator == '/':
            result = a // b if b != 0 else 'Error'
        
        self.stack.append(result)

    def get_display(self):
        if self.current_input:
            return self.current_input
        elif self.stack:
            return str(self.stack[-1])
        return "0"

# GUI Implementation
class CalculatorGUI:
    def __init__(self, root, calc_logic, logger):
        self.logic = calc_logic
        self.logger = logger
        self.root = root
        self.root.title("RPN Calculator")
        
        self.display = tk.Entry(root, font=('Arial', 20), borderwidth=5, relief="ridge", justify='right')
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.update_display()
        
        # Define button texts including 'Enter' for RPN operation
        buttons = [
            '7', '8', '9', '+',
            '4', '5', '6', '-',
            '1', '2', '3', 'x',
            'C', '0', 'Enter', '/'
        ]
        
        for i, text in enumerate(buttons):
            button = tk.Button(root, text=text, font=('Arial', 20), width=4, command=lambda t=text: self.on_button_press(t))
            row = (i // 4) + 1
            col = i % 4
            button.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        
        for i in range(1, 5):
            root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)

    def on_button_press(self, key):
        self.logic.press(key)
        self.update_display()
        self.logger.log_keypress(key)

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.logic.get_display())

# Setup and run the calculator
logger = KeypressLogger('user2', 'case2')
rpn_logic = RPNCalculator()
root = tk.Tk()
app = CalculatorGUI(root, rpn_logic, logger)
root.mainloop()
