import tkinter as tk
from tkinter import ttk, messagebox
import random


def get_warmth_clue(difference: int) -> tuple[str, str]:
    """
    Given how far off the guess is, return a (label, hex_color) tuple.
    The color visually reinforces how close the user is.
    """
    if difference > 40:
        return "🧊 Ice Cold!", "#74b9ff"       
    elif difference > 20:
        return "❄️  Cold", "#a29bfe"           
    elif difference > 10:
        return "😐 Warm", "#fdcb6e"          
    elif difference > 5:
        return "🔥 Hot!", "#e17055"             
    else:
        return "🌋 Burning! Very close!", "#d63031"  


def generate_math_clues(number: int) -> list[str]:
    """
    Build a list of 4 math-based clues about `number`.
    They are revealed one by one as the game progresses,
    so the order matters — put the most informative ones later.
    """
    clues = []

    # Clue 1 (revealed at start) — easiest, halves the range
    clues.append(
        f"The number is {'greater than' if number > 50 else '50 or less than'} 50"
    )

    # Clue 2 (after 3 wrong guesses) — eliminates half the remaining numbers
    clues.append(
        f"The number is {'even' if number % 2 == 0 else 'odd'}"
    )

    # Clue 3 (after 6 wrong guesses) — gives divisibility info
    if number % 5 == 0:
        clues.append("The number is divisible by 5")
    elif number % 3 == 0:
        clues.append("The number is divisible by 3")
    else:
        clues.append("The number is NOT divisible by 3 or 5")

    # Clue 4 (after 9 wrong guesses) — most specific, gives exact digit sum
    digit_sum = sum(int(d) for d in str(number))
    clues.append(f"The sum of its digits is {digit_sum}")

    return clues

# GUI

class NumberGuessingGame:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("460x570")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f6f8")

        # Game state — these are the variables that persist between button clicks
        self.secret_number: int = 0
        self.attempts: int = 0
        self.clues_revealed: int = 0
        self.math_clues: list[str] = []
        self.game_over: bool = False

        self._build_widgets()   # create all widgets once
        self.start_new_game()   # populate them with a fresh game

    # Game logic 

    def start_new_game(self):
        """Reset ALL game state and refresh the UI for a brand-new round."""
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.game_over = False
        self.math_clues = generate_math_clues(self.secret_number)
        self.clues_revealed = 1       # always reveal the first clue immediately

        # Reset all labels / widgets to their blank starting state
        self.attempts_label.config(text="Attempts: 0")
        self.warmth_label.config(text="Make your first guess!", fg="#636e72")
        self.direction_label.config(text="")
        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.submit_btn.config(state="normal")

        self._refresh_clue_panel()

    def on_submit(self):
    
        if self.game_over:
            
            messagebox.showinfo("Game over", "Click 🔄 Play Again to start a new round!")
            return

        raw = self.entry.get().strip()

        # Validation 
        if not raw:
            messagebox.showwarning("Empty input", "Please type a number first.")
            return

        try:
            guess = int(raw)     # int() rejects decimals AND letters
        except ValueError:
            messagebox.showerror(
                "Invalid input",
                "Please enter a whole number — no letters or decimal points."
            )
            self.entry.delete(0, tk.END)
            return

        if guess < 1 or guess > 100:
            messagebox.showwarning(
                "Out of range",
                "Please enter a number between 1 and 100."
            )
            self.entry.delete(0, tk.END)
            return

        # Core game logic 
        self.attempts += 1
        self.attempts_label.config(text=f"Attempts: {self.attempts}")
        self.entry.delete(0, tk.END)

        difference = abs(guess - self.secret_number)

        if difference == 0:
            self._show_win()
        else:
            self._show_clues(guess, difference)

            # Unlock a new math clue every 3 wrong attempts (max 4 clues total)
            new_clue_index = self.attempts // 3          # 3 → 1, 6 → 2, 9 → 3
            if new_clue_index >= self.clues_revealed and self.clues_revealed < len(self.math_clues):
                self.clues_revealed += 1
                self._refresh_clue_panel()

    def _show_win(self):
        attempt_word = "attempt" if self.attempts == 1 else "attempts"
        self.warmth_label.config(
            text=f"🎉 Correct!", fg="#00b894"
        )
        self.direction_label.config(
            text=f"You got it in {self.attempts} {attempt_word}!",
            fg="#00b894"
        )
        self.game_over = True
        self.entry.config(state="disabled")
        self.submit_btn.config(state="disabled")

    def _show_clues(self, guess: int, difference: int):
        warmth_text, warmth_color = get_warmth_clue(difference)
        direction = "Go Higher ⬆️" if guess < self.secret_number else "Go Lower ⬇️"

        self.warmth_label.config(text=warmth_text, fg=warmth_color)
        self.direction_label.config(text=direction, fg="#1f2933")

    def _refresh_clue_panel(self):
        lines = []
        for i in range(self.clues_revealed):
            lines.append(f"  ✅  {self.math_clues[i]}")

        locked = len(self.math_clues) - self.clues_revealed
        if locked > 0:
            next_unlock = (self.clues_revealed) * 3   
            lines.append(f"  🔒  {locked} more unlock{'s' if locked == 1 else ''} "
                         f"every 3 guesses...")

        self.clue_text_label.config(text="\n".join(lines))

    # Widget construction 

    def _build_widgets(self):
        """Create every widget once. Values are populated by start_new_game()."""

        # Title 
        tk.Label(
            self.root, text="🎯 Number Guessing Game",
            font=("Segoe UI", 17, "bold"), bg="#f4f6f8", fg="#1f2933"
        ).pack(pady=(22, 2))

        tk.Label(
            self.root, text="Guess a number between 1 and 100",
            font=("Segoe UI", 10), bg="#f4f6f8", fg="#616e7c"
        ).pack(pady=(0, 14))

        # Math clues panel
        clues_frame = tk.LabelFrame(
            self.root, text="📐 Math Clues",
            font=("Segoe UI", 10, "bold"),
            bg="#f4f6f8", padx=12, pady=10
        )
        clues_frame.pack(padx=30, fill="x", pady=(0, 14))

        self.clue_text_label = tk.Label(
            clues_frame, text="",
            font=("Segoe UI", 10), bg="#f4f6f8",
            fg="#2d3436", justify="left", anchor="w"
        )
        self.clue_text_label.pack(fill="x")

        
        input_frame = tk.Frame(self.root, bg="#f4f6f8")
        input_frame.pack(pady=8)

        self.entry = ttk.Entry(
            input_frame, font=("Segoe UI", 14),
            width=8, justify="center"
        )
        self.entry.grid(row=0, column=0, padx=(0, 10))
        self.entry.bind("<Return>", lambda e: self.on_submit())

        self.submit_btn = ttk.Button(
            input_frame, text="Submit Guess", command=self.on_submit
        )
        self.submit_btn.grid(row=0, column=1)

        
        self.warmth_label = tk.Label(
            self.root, text="",
            font=("Segoe UI", 22, "bold"), bg="#f4f6f8"
        )
        self.warmth_label.pack(pady=(18, 2))

        
        self.direction_label = tk.Label(
            self.root, text="",
            font=("Segoe UI", 13, "bold"), bg="#f4f6f8", fg="#1f2933"
        )
        self.direction_label.pack(pady=(0, 10))

       
        self.attempts_label = tk.Label(
            self.root, text="Attempts: 0",
            font=("Segoe UI", 10), bg="#f4f6f8", fg="#636e72"
        )
        self.attempts_label.pack(pady=(0, 18))

       
        ttk.Button(
            self.root, text="🔄  Play Again", command=self.start_new_game
        ).pack()

# Entry point

def main():
    root = tk.Tk()
    NumberGuessingGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()