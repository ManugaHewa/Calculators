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

# Define the calculator class based on the statechart
class CalculatorStatechart:
    def __init__(self):
        self.reset_state()

    def reset_state(self):
        self.state = "Start/Idle"
        self.current = "0"
        self.operation = ""
        self.accumulator = 0

    def press(self, key):
        if key.isdigit():
            if self.state == "Start/Idle" or self.state == "Operation Input":
                self.current = key
                self.state = "Number Input"
            else:
                self.current += key
        elif key in ['+', '-', 'x', '/']:
            if self.state == "Number Input":
                self.compute()
            self.operation = key
            self.state = "Operation Input"
        elif key == '=':
            self.compute()
            self.state = "Result display"
            self.operation = ""
        elif key == 'C':
            self.reset_state()

    def compute(self):
        if self.operation:
            if self.operation == '+':
                self.accumulator += int(self.current)
            elif self.operation == '-':
                self.accumulator -= int(self.current)
            elif self.operation == 'x':
                self.accumulator *= int(self.current)
            elif self.operation == '/':
                self.accumulator //= int(self.current)
        else:
            self.accumulator = int(self.current)
        self.current = "0"

    def get_display(self):
        if self.state == "Result display":
            return str(self.accumulator)
        elif self.current != "0":
            return self.current
        else:
            return str(self.accumulator)
        
# Implement a simple GUI for the calculator using tkinter
class CalculatorGUI:
    def __init__(self, root, calc_logic, logger):
        self.logic = calc_logic
        self.logger = logger
        self.root = root
        self.root.title("Statechart Calculator")
        
        self.display = tk.Entry(root, font=('Arial', 20), borderwidth=5, relief="ridge", justify='right')
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.display.insert(0, '0')
        
        # Define button texts in a list
        buttons = [
            '7', '8', '9', '+',
            '4', '5', '6', '-',
            '1', '2', '3', 'x',
            'C', '0', '=', '/'
        ]
        
        # Create buttons using a loop
        for i, text in enumerate(buttons):
            button = tk.Button(self.root, text=text, font=('Arial', 20), width=4, command=lambda t=text: self.on_button_press(t))
            row = (i // 4) + 1
            col = i % 4
            button.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        
        # Configure grid weights
        for i in range(1, 5):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
        
    def on_button_press(self, key):
        self.logic.press(key)
        self.display.delete(0, tk.END)
        self.display.insert(0, self.logic.get_display())
        self.logger.log_keypress(key)  # Log each keypress

logger = KeypressLogger('user1', 'case1')

# Instantiate the calculator logic.
calc_logic = CalculatorStatechart()

# Set up the main application window.
root = tk.Tk()

# Instantiate the GUI with the root window, calculator logic, and logger.
app = CalculatorGUI(root, calc_logic, logger)

# Run the calculator application.
root.mainloop()
