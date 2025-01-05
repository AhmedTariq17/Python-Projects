import random  # Importing the random module for random number generation

# Constants for the slot machine
MAX_LINES = 3  # Maximum number of lines a user can bet on
MAX_BET = 100  # Maximum bet amount per line
MIN_BET = 1  # Minimum bet amount per line

# Dimensions of the slot machine
ROWS = 3  # Number of rows in the slot machine
COLS = 3  # Number of columns in the slot machine

# Configuration of symbols and their counts
symbol_count = {
    "A": 2,  # Symbol 'A' appears 2 times
    "B": 4,  # Symbol 'B' appears 4 times
    "C": 6,  # Symbol 'C' appears 6 times
    "D": 8   # Symbol 'D' appears 8 times
}

# Values associated with each symbol for winnings
symbol_value = {
    "A": 5,  # Symbol 'A' has a value of 5
    "B": 4,  # Symbol 'B' has a value of 4
    "C": 3,  # Symbol 'C' has a value of 3
    "D": 2   # Symbol 'D' has a value of 2
}

# Function to calculate winnings based on the slot machine's result
def check_winnings(columns, lines, bet, values):
    """
    Check if the player has won and calculate the total winnings.
    :param columns: List of columns from the slot machine spin
    :param lines: Number of lines the player is betting on
    :param bet: Bet amount per line
    :param values: Dictionary mapping symbols to their values
    :return: Total winnings and the winning lines
    """
    winnings = 0
    winnings_lines = []
    for line in range(lines):
        symbol = columns[0][line]  # Get the symbol in the first column for the line
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:  # Check if all symbols in the line match
                break
        else:
            # If all symbols in the line match, calculate winnings
            winnings += values[symbol] * bet
            winnings_lines.append(line + 1)  # Store the winning line (1-indexed)

    return winnings, winnings_lines

# Function to generate a random slot machine spin
def get_slot_machine_spin(rows, cols, symbols):
    """
    Generate a random spin for the slot machine.
    :param rows: Number of rows in the slot machine
    :param cols: Number of columns in the slot machine
    :param symbols: Dictionary of symbols and their counts
    :return: List of columns representing the slot machine spin
    """
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        # Add each symbol to the list according to its count
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]  # Make a copy of the symbols list
        for _ in range(rows):
            value = random.choice(current_symbols)  # Randomly select a symbol
            current_symbols.remove(value)  # Remove the symbol to avoid repetition
            column.append(value)

        columns.append(column)

    return columns

# Function to display the slot machine columns
def print_slot_machine(columns):
    """
    Print the slot machine columns in a formatted manner.
    :param columns: List of columns to display
    """
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")  # Print with separators
            else:
                print(column[row], end="")  # Print last column without separator
        print()  # Newline after each row

# Function to get the deposit amount from the user
def deposit():
    """
    Prompt the user to deposit money and validate the input.
    :return: Validated deposit amount
    """
    while True:
        amount = input("What would you like to deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:  # Ensure the deposit is greater than 0
                break
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a number.")

    return amount

# Function to get the number of lines the user wants to bet on
def get_number_of_lines():
    """
    Prompt the user to select the number of lines to bet on.
    :return: Validated number of lines
    """
    while True:
        lines = input(f"Enter the number of lines to bet on (1-{MAX_LINES})? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:  # Ensure the input is within the valid range
                break
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a number.")

    return lines

# Function to get the bet amount per line
def get_bet():
    """
    Prompt the user to enter the bet amount per line and validate the input.
    :return: Validated bet amount
    """
    while True:
        amount = input("What would you like to bet on each line? $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:  # Ensure the bet is within the valid range
                break
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}.")
        else:
            print("Please enter a number.")

    return amount

# Function to handle a single spin of the slot machine
def spin(balance):
    """
    Handle the logic for a single spin of the slot machine.
    :param balance: Current balance of the player
    :return: Net winnings (winnings minus total bet)
    """
    lines = get_number_of_lines()  # Get the number of lines to bet on
    while True:
        bet = get_bet()  # Get the bet amount per line
        total_bet = bet * lines  # Calculate total bet

        if total_bet > balance:
            # Check if the user has enough balance to make the bet
            print(f"You do not have enough to bet that amount, your current balance is: ${balance}")
        else:
            break

    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}")

    # Generate and display the slot machine spin
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)

    # Check winnings and display results
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}.")
    print(f"You won on lines:", *winning_lines)

    return winnings - total_bet  # Return net winnings

# Main game loop
def main():
    """
    Main function to run the slot machine game.
    """
    balance = deposit()  # Get the initial deposit from the user
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to play (q to quit).")  # Prompt user to play or quit
        if answer == "q":
            break  # Exit the game loop if the user quits
        balance += spin(balance)  # Update balance after each spin

    print(f"You left with ${balance}")  # Display final balance


main()  # Run the main game function
