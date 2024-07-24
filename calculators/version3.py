import tkinter as tk
from datetime import datetime
import csv
import re

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

# SafeEvalCalculator logic
class SafeEvalCalculator:
    def __init__(self):
        self.current_input = ""

    def press(self, key):
        if key in '0123456789+-x/().':
            # Replace 'x' with '*' for multiplication
            self.current_input += key.replace('x', '*')
        elif key == '=':
            self.current_input = str(self.safe_eval(self.current_input))
        elif key == 'C':
            self.current_input = ""

    def safe_eval(self, expr):
        # Sanitize the input expression to contain only numbers, operators, and parentheses
        sanitized_expr = re.sub('[^0-9+*/().-]', '', expr)
        try:
            # Evaluate the sanitized expression
            return eval(sanitized_expr)
        except Exception:
            return "Error"

    def get_display(self):
        return self.current_input if self.current_input else "0"

# GUI Implementation
class CalculatorGUI:
    def __init__(self, root, calc_logic, logger):
        self.logic = calc_logic
        self.logger = logger
        self.root = root
        self.root.title("Advanced Calculator")
        
        self.display = tk.Entry(root, font=('Arial', 20), borderwidth=5, relief="ridge", justify='right')
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.update_display()
        
        # Define button texts including parentheses for this version
        buttons = [
            '7', '8', '9', '+',
            '4', '5', '6', '-',
            '1', '2', '3', 'x',
            'C', '0', '=', '/',
            '(', ')', ' ', ' '  # Add support for parentheses; the last two are placeholders
        ]
        
        for i, text in enumerate(buttons):
            if text.strip():  # Skip placeholders
                button = tk.Button(root, text=text, font=('Arial', 20), width=4, command=lambda t=text: self.on_button_press(t))
                row = (i // 4) + 1
                col = i % 4
                button.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        
        for i in range(1, 6):  # Adjust row range for the extra row
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
logger = KeypressLogger('user3', 'case3')
calc_logic = SafeEvalCalculator()
root = tk.Tk()
app = CalculatorGUI(root, calc_logic, logger)
root.mainloop()
