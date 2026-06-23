# SCT_SD_2
Number Guessing Game

A desktop GUI game built with Python and Tkinter where the user guesses a randomly
generated number between 1 and 100, guided by two types of clues after every guess.

Features:
1. Random number generated fresh each round (1–100)
2. Warmth clues after every guess — 5 levels from Ice Cold to Burning
3. Math clues unlocked progressively every 3 wrong guesses (up to 4 clues)
4. Attempt counter to track how many guesses it took
5. Input validation — handles empty input, letters, decimals, and out-of-range numbers
6. Play Again button to restart instantly without reopening the app


Clue System -

1. Warmth Clues (shown after every guess)
Distance from secret Label 
More than 40 away : 🧊 Ice Cold!
21 – 40 away❄️ Cold
11 – 20 away😐 Warm
6 – 10 away🔥 Hot!
1 – 5 away🌋 Burning! Very close!

2. Math Clues (unlocked progressively)
Unlocks at attempt    Clue
Game start            Is the number above or below 50?
Attempt 3             Is the number even or odd?
Attempt 6             Is it divisible by 3 or 5?
Attempt 9             What is the sum of its digits?

Tech used:
Python 3
Tkinter (built into Python's standard library — no extra installs needed)
random module (built-in)
