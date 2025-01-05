# Slots Game

This project is a command-line implementation of a slot machine game in Python. Players can deposit money, place bets on lines, and spin the slot machine to win based on matching symbols.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Game Rules](#game-rules)
- [Screenshots](#screenshots)
- [License](#license)

## Features
- Interactive command-line interface.
- Players can deposit money and bet on up to 3 lines.
- Randomized slot machine spins with configurable symbol frequencies.
- Calculates winnings based on bet amount and matching symbols.
- Displays the current balance after each spin.

## Technologies Used
- **Programming Language:** Python
- **Standard Library:** `random` (for generating random spins)

## Installation

### Prerequisites
- Python 3.7+

### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/slots-game.git
   cd slots-game
   ```

2. **Run the game:**
   ```bash
   python main.py
   ```

## Usage
- Launch the game by running the `main.py` file.
- Follow the prompts to deposit money, select the number of lines, and place your bets.
- Spin the slot machine and check your winnings.
- Quit the game at any time by pressing `q`.

## File Structure
```
.
├── main.py              # Main game code
└── README.md            # Project documentation
```

## Game Rules
1. **Deposit Money:** Players must deposit money to start playing.
2. **Select Lines:** Players can bet on 1 to 3 lines.
3. **Place Bets:** Bet amounts must be between $1 and $100 per line.
4. **Spin the Machine:** The slot machine will generate random symbols for each column and row.
5. **Winnings:**
   - Players win if all symbols on a selected line match.
   - Winnings are calculated as `symbol value × bet amount`.
   - Each symbol has a different value:
     - `A`: 5
     - `B`: 4
     - `C`: 3
     - `D`: 2
6. **Balance Updates:** The total bet amount is deducted, and winnings are added to the balance.
7. **Game End:** Players can quit anytime by pressing `q`.

## Screenshots
### Starting the Game
```
What would you like to deposit? $100
Current balance is $100
Press enter to play (q to quit).
```

### Placing a Bet
```
Enter the number of lines to bet on (1-3)? 3
What would you like to bet on each line? $10
You are betting $10 on 3 lines. Total bet is equal to: $30
```

### Slot Machine Spin
```
A | B | C
B | A | D
D | B | A
You won $20.
You won on lines: 1 2
```

### Ending the Game
```
Press enter to play (q to quit).
q
You left with $90
```

## License
This project is licensed under the MIT License. You are free to use, modify, and distribute this software as long as the original license is included.

---
Feel free to contribute to the project or report issues by opening a pull request or an issue on GitHub!

