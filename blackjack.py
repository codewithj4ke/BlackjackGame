import tkinter as tk
from tkinter import messagebox
import random
import time

# Define the logo
logo = """
.------.            _     _            _    _            _    
|A_  _ |.          | |   | |          | |  (_)          | |   
|( \/ ).-----.     | |__ | | __ _  ___| | ___  __ _  ___| | __
| \  /|K /\  |     | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
|  \/ | /  \ |     | |_) | | (_| | (__|   <| | (_| | (__|   < 
`-----| \  / |     |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\\
      |  \/ K|                            _/ |                
      `------'                           |__/           
"""


def deal_card():
    """Return a random card value."""
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]  # Possible card values including face cards
    return random.choice(cards)  # Randomly select a card value


def calculate_score(cards):
    """Calculate and return the score of the given list of cards."""
    if sum(cards) == 21 and len(cards) == 2:
        return 0  # Blackjack (special case where score is 21 with only 2 cards)

    if 11 in cards and sum(cards) > 21:
        # Adjust for ace value if the score goes over 21
        cards.remove(11)
        cards.append(1)
    return sum(cards)  # Return the total score of the cards


def compare(user_score, computer_score):
    """Compare user and computer scores and return the result."""
    if user_score > 21:
        return "You went over. You lose 😭", "#F44336"  # Red color for loss

    if computer_score > 21:
        return "Opponent went over. You win 😁", "#4CAF50"  # Green color for win

    if user_score == computer_score:
        return "Draw 🙃", "#FFC107"  # Yellow color for draw

    if user_score == 0:
        return "Win with a Blackjack 😎", "#4CAF50"  # Green color for win with blackjack

    if computer_score == 0:
        return "Lose, opponent has Blackjack 😱", "#F44336"  # Red color for loss with opponent's blackjack

    if user_score > computer_score:
        return "You win 😃", "#4CAF50"  # Green color for win

    return "You lose 😤", "#F44336"  # Red color for loss


class BlackjackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Game")  # Set the title of the window
        self.root.geometry("600x500")  # Set the size of the window
        self.root.resizable(False, False)  # Disable resizing of the window

        # Define styles for the application
        self.style = {
            "font": ("Lato", 12),
            "font_bold": ("Lato", 12, "bold"),
            "bg": "#2C3E50",
            "fg": "#ECF0F1",
            "button_bg": "#3498DB",
            "button_fg": "#fff",
            "button_hover_bg": "#2980B9",
            "button_hover_fg": "#fff",
            "padx": 12,
            "pady": 8,
            "button_padx": 24,
            "button_pady": 12
        }

        # Initialize game statistics
        self.stats = {
            "games_played": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0.0
        }

        # Create and configure main frame
        self.frame = tk.Frame(root, bg=self.style["bg"])
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Scoreboard Section
        self.scoreboard_frame = tk.Frame(self.frame, bg=self.style["bg"])
        self.scoreboard_frame.grid(row=0, column=0, columnspan=4, pady=(0, 20), sticky="ew")
        self.scoreboard_frame.grid_columnconfigure(0, weight=1)
        self.scoreboard_frame.grid_columnconfigure(1, weight=1)
        self.scoreboard_frame.grid_columnconfigure(2, weight=1)
        self.scoreboard_frame.grid_columnconfigure(3, weight=1)

        # Create labels to display game statistics
        self.games_played_label = tk.Label(
            self.scoreboard_frame, text="Games Played: 0", font=self.style["font_bold"], bg=self.style["bg"],
            fg="#ECF0F1"
        )
        self.games_played_label.grid(row=0, column=0, padx=10, sticky="ew")

        self.wins_label = tk.Label(
            self.scoreboard_frame, text="Wins: 0", font=self.style["font_bold"], bg=self.style["bg"], fg="#ECF0F1"
        )
        self.wins_label.grid(row=0, column=1, padx=10, sticky="ew")

        self.losses_label = tk.Label(
            self.scoreboard_frame, text="Losses: 0", font=self.style["font_bold"], bg=self.style["bg"], fg="#ECF0F1"
        )
        self.losses_label.grid(row=0, column=2, padx=10, sticky="ew")

        self.win_rate_label = tk.Label(
            self.scoreboard_frame, text="Win Rate: 0%", font=self.style["font_bold"], bg=self.style["bg"], fg="#ECF0F1"
        )
        self.win_rate_label.grid(row=0, column=3, padx=10, sticky="ew")

        # Game UI elements
        self.logo_label = tk.Label(
            self.frame, text=logo, font=("Courier", 10), bg=self.style["bg"], fg="#F1C40F", justify="left"
        )
        self.logo_label.grid(row=1, column=0, columnspan=3, pady=(0, 20), sticky="w")

        self.result_label = tk.Label(
            self.frame, text="", font=self.style["font"], bg=self.style["bg"], fg="#ECF0F1"
        )
        self.result_label.grid(row=2, column=0, columnspan=3, pady=10)

        self.user_cards_label = tk.Label(
            self.frame, text="Your cards: []", font=self.style["font"], bg=self.style["bg"], fg="#ECF0F1"
        )
        self.user_cards_label.grid(row=3, column=0, columnspan=3, pady=5)

        self.computer_cards_label = tk.Label(
            self.frame, text="Computer's cards: []", font=self.style["font"], bg=self.style["bg"], fg="#ECF0F1"
        )
        self.computer_cards_label.grid(row=4, column=0, columnspan=3, pady=5)

        # Create buttons for game actions
        self.deal_button = tk.Button(
            self.frame, text="Deal", command=self.start_game, bg=self.style["button_bg"], fg=self.style["button_fg"],
            padx=self.style["button_padx"], pady=self.style["button_pady"], font=("Lato", 14, "bold")
        )
        self.deal_button.grid(row=5, column=0, pady=10, padx=(0, 10), sticky="ew")
        self.add_hover_effect(self.deal_button, self.style["button_bg"], self.style["button_hover_bg"])

        self.hit_button = tk.Button(
            self.frame, text="Hit", command=self.hit, state=tk.DISABLED, bg="#F39C12", fg="#000",
            padx=self.style["button_padx"], pady=self.style["button_pady"], font=("Lato", 14, "bold")
        )
        self.hit_button.grid(row=5, column=1, pady=10, padx=(0, 10), sticky="ew")
        self.add_hover_effect(self.hit_button, "#F39C12", "#F1C40F")

        self.stand_button = tk.Button(
            self.frame, text="Stand", command=self.stand, state=tk.DISABLED, bg="#E74C3C", fg="#fff",
            padx=self.style["button_padx"], pady=self.style["button_pady"], font=("Lato", 14, "bold")
        )
        self.stand_button.grid(row=5, column=2, pady=10, sticky="ew")
        self.add_hover_effect(self.stand_button, "#E74C3C", "#C0392B")

        # Make buttons expand equally
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)

    def add_hover_effect(self, button, original_bg, hover_bg):
        """Add hover effect to change button background color on mouse enter and leave."""
        button.bind("<Enter>", lambda e: button.config(bg=hover_bg))
        button.bind("<Leave>", lambda e: button.config(bg=original_bg))

    def start_game(self):
        """Start a new game of Blackjack."""
        self.user_cards = [deal_card(), deal_card()]
        self.computer_cards = [deal_card(), deal_card()]

        self.update_cards_display()
        self.check_for_blackjack()

        # Enable the hit and stand buttons
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.deal_button.config(state=tk.DISABLED)

        # Increment games played
        self.stats["games_played"] += 1
        self.update_stats()

    def check_for_blackjack(self):
        """Check if either player or computer has Blackjack."""
        if calculate_score(self.user_cards) == 0:
            self.end_game("You got a Blackjack! 😎", "#4CAF50")
        elif calculate_score(self.computer_cards) == 0:
            self.end_game("Opponent got a Blackjack! 😱", "#F44336")

    def hit(self):
        """Give the player an additional card."""
        self.user_cards.append(deal_card())
        self.update_cards_display()

        if calculate_score(self.user_cards) > 21:
            self.end_game("You went over. You lose 😭", "#F44336")

    def stand(self):
        """End the player's turn and let the computer play."""
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)

        while calculate_score(self.computer_cards) < 17:
            self.computer_cards.append(deal_card())

        self.update_cards_display()
        self.end_game(*compare(calculate_score(self.user_cards), calculate_score(self.computer_cards)))

    def update_cards_display(self):
        """Update the display of user and computer cards and their scores."""
        user_score = calculate_score(self.user_cards)
        computer_score = calculate_score(self.computer_cards)

        self.user_cards_label.config(text=f"Your cards: {self.user_cards} (Score: {user_score})")
        self.computer_cards_label.config(text=f"Computer's cards: {self.computer_cards} (Score: {computer_score})")

    def end_game(self, result_message, color):
        """End the game and display the result."""
        self.result_label.config(text=result_message, fg=color)
        self.deal_button.config(state=tk.NORMAL)

        # Update game statistics
        if color == "#4CAF50":
            self.stats["wins"] += 1
        elif color == "#F44336":
            self.stats["losses"] += 1

        self.stats["win_rate"] = (self.stats["wins"] / self.stats["games_played"]) * 100 if self.stats[
                                                                                                "games_played"] > 0 else 0
        self.update_stats()

    def update_stats(self):
        """Update the game statistics display."""
        self.games_played_label.config(text=f"Games Played: {self.stats['games_played']}")
        self.wins_label.config(text=f"Wins: {self.stats['wins']}")
        self.losses_label.config(text=f"Losses: {self.stats['losses']}")
        self.win_rate_label.config(text=f"Win Rate: {self.stats['win_rate']:.1f}%")


if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackApp(root)
    root.mainloop()
