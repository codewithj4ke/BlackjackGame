# Project: Blackjack Game
# Application developed by: codewithj4ke - September 2024
# Learning Python programming with the assistance of AI and online courses

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
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)

def calculate_score(cards):
    """Calculate and return the score of the given list of cards."""
    if sum(cards) == 21 and len(cards) == 2:
        return 0  # Blackjack

    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)
    return sum(cards)

def compare(user_score, computer_score):
    """Compare user and computer scores and return the result."""
    if user_score > 21:
        return "You went over. You lose 😭", "#F44336"  # Red for loss

    if computer_score > 21:
        return "Opponent went over. You win 😁", "#4CAF50"  # Green for win

    if user_score == computer_score:
        return "Draw 🙃", "#FFC107"  # Yellow for draw

    if user_score == 0:
        return "Win with a Blackjack 😎", "#4CAF50"  # Green for win

    if computer_score == 0:
        return "Lose, opponent has Blackjack 😱", "#F44336"  # Red for loss

    if user_score > computer_score:
        return "You win 😃", "#4CAF50"  # Green for win

    return "You lose 😤", "#F44336"  # Red for loss

class BlackjackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Game")
        self.root.geometry("800x600")  # Increased height for scoreboard
        self.root.resizable(False, False)

        self.style = {
            "font": ("Arial", 12),
            "font_bold": ("Arial", 12, "bold"),
            "bg": "#333",
            "fg": "#fff",
            "button_bg": "#4CAF50",
            "button_fg": "#fff",
            "button_hover_bg": "#45A049",
            "button_hover_fg": "#fff",
            "padx": 10,
            "pady": 5,
            "button_padx": 20,
            "button_pady": 10
        }

        self.stats = {
            "games_played": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0.0
        }

        self.frame = tk.Frame(root, bg=self.style["bg"])
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Scoreboard Section
        self.scoreboard_frame = tk.Frame(self.frame, bg=self.style["bg"])
        self.scoreboard_frame.grid(row=0, column=0, columnspan=4, pady=(0, 20), sticky="ew")

        self.games_played_label = tk.Label(
            self.scoreboard_frame, text="Games Played: 0", font=self.style["font_bold"], bg=self.style["bg"], fg="#FFEB3B"
        )
        self.games_played_label.grid(row=0, column=0, padx=10)

        self.wins_label = tk.Label(
            self.scoreboard_frame, text="Wins: 0", font=self.style["font_bold"], bg=self.style["bg"], fg="#FFEB3B"
        )
        self.wins_label.grid(row=0, column=1, padx=10)

        self.losses_label = tk.Label(
            self.scoreboard_frame, text="Losses: 0", font=self.style["font_bold"], bg=self.style["bg"], fg="#FFEB3B"
        )
        self.losses_label.grid(row=0, column=2, padx=10)

        self.win_rate_label = tk.Label(
            self.scoreboard_frame, text="Win Rate: 0%", font=self.style["font_bold"], bg=self.style["bg"], fg="#FFEB3B"
        )
        self.win_rate_label.grid(row=0, column=3, padx=10)

        # Game UI
        self.logo_label = tk.Label(
            self.frame, text=logo, font=("Courier", 10), bg=self.style["bg"], fg="#FFD700", justify="left"
        )
        self.logo_label.grid(row=1, column=0, columnspan=3, pady=(0, 20), sticky="w")

        self.result_label = tk.Label(
            self.frame, text="", font=self.style["font"], bg=self.style["bg"], fg="#FFEB3B"
        )
        self.result_label.grid(row=2, column=0, columnspan=3, pady=10)

        self.user_cards_label = tk.Label(
            self.frame, text="Your cards: []", font=self.style["font"], bg=self.style["bg"], fg="#FFEB3B"
        )
        self.user_cards_label.grid(row=3, column=0, columnspan=3, pady=5)

        self.computer_cards_label = tk.Label(
            self.frame, text="Computer's cards: []", font=self.style["font"], bg=self.style["bg"], fg="#FFEB3B"
        )
        self.computer_cards_label.grid(row=4, column=0, columnspan=3, pady=5)

        self.deal_button = tk.Button(
            self.frame, text="Deal", command=self.start_game, bg=self.style["button_bg"], fg=self.style["button_fg"],
            padx=self.style["button_padx"], pady=self.style["button_pady"], font=("Arial", 14, "bold")
        )
        self.deal_button.grid(row=5, column=0, pady=10, padx=(0, 10), sticky="ew")
        self.add_hover_effect(self.deal_button, self.style["button_bg"], self.style["button_hover_bg"])

        self.hit_button = tk.Button(
            self.frame, text="Hit", command=self.hit, state=tk.DISABLED, bg="#FFC107", fg="#000",
            padx=self.style["button_padx"], pady=self.style["button_pady"], font=("Arial", 14, "bold")
        )
        self.hit_button.grid(row=5, column=1, pady=10, padx=(0, 10), sticky="ew")
        self.add_hover_effect(self.hit_button, "#FFC107", "#FFB300")

        self.stand_button = tk.Button(
            self.frame, text="Stand", command=self.stand, state=tk.DISABLED, bg="#F44336", fg="#fff",
            padx=self.style["button_padx"], pady=self.style["button_pady"], font=("Arial", 14, "bold")
        )
        self.stand_button.grid(row=5, column=2, pady=10, sticky="ew")
        self.add_hover_effect(self.stand_button, "#F44336", "#E53935")

        # Make buttons expand equally
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)

    def add_hover_effect(self, button, original_bg, hover_bg):
        button.bind("<Enter>", lambda e: button.config(bg=hover_bg))
        button.bind("<Leave>", lambda e: button.config(bg=original_bg))

    def start_game(self):
        self.user_cards = [deal_card(), deal_card()]
        self.computer_cards = [deal_card(), deal_card()]
        self.is_game_over = False
        self.update_labels()

        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)

    def hit(self):
        if not self.is_game_over:
            self.user_cards.append(deal_card())
            user_score = calculate_score(self.user_cards)
            if user_score > 21:
                self.is_game_over = True
                self.result_label.config(text="You went over. You lose 😭", fg="#F44336")
                self.update_statistics()
                self.animate_loss()
            self.update_labels()

    def stand(self):
        if not self.is_game_over:
            while calculate_score(self.computer_cards) < 17:
                self.computer_cards.append(deal_card())
            self.is_game_over = True
            user_score = calculate_score(self.user_cards)
            computer_score = calculate_score(self.computer_cards)
            result, color = compare(user_score, computer_score)
            self.result_label.config(text=result, fg=color)
            self.update_statistics()
            if color == "#F44336":
                self.animate_loss()

    def update_labels(self):
        user_score = calculate_score(self.user_cards)
        computer_score = calculate_score(self.computer_cards)
        self.user_cards_label.config(text=f"Your cards: {self.user_cards} (Score: {user_score})")
        self.computer_cards_label.config(text=f"Computer's cards: {self.computer_cards} (Score: {computer_score})")

    def update_statistics(self):
        self.stats["games_played"] += 1
        if self.result_label.cget("fg") == "#4CAF50":
            self.stats["wins"] += 1
        elif self.result_label.cget("fg") == "#F44336":
            self.stats["losses"] += 1
        self.stats["win_rate"] = (self.stats["wins"] / self.stats["games_played"]) * 100 if self.stats["games_played"] > 0 else 0.0

        self.games_played_label.config(text=f"Games Played: {self.stats['games_played']}")
        self.wins_label.config(text=f"Wins: {self.stats['wins']}")
        self.losses_label.config(text=f"Losses: {self.stats['losses']}")
        self.win_rate_label.config(text=f"Win Rate: {self.stats['win_rate']:.1f}%")

    def animate_loss(self):
        for _ in range(5):
            self.result_label.config(fg="#F44336")
            self.root.update()
            time.sleep(0.1)
            self.result_label.config(fg="#FFEB3B")
            self.root.update()
            time.sleep(0.1)

if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackApp(root)
    root.mainloop()
