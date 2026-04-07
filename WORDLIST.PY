import random
import os
from typing import List, Tuple

class WordGuessGame:
    def __init__(self, wordlist_file: str = "WORDLIST.TXT"):
        """Initialize the word guessing game."""
        self.wordlist_file = wordlist_file
        self.words = self.load_words()
        self.questions = self.load_questions()
        self.secret_word = ""
        self.current_question = ""
        self.max_attempts = 6
        self.attempts = []
        
    def load_questions(self) -> dict:
        """Load questions/clues for each word."""
        questions = {
            "APPLE": "What red or green fruit grows on trees?",
            "BEACH": "Where do you go to swim in the ocean?",
            "BRAVE": "What word means courageous or fearless?",
            "CLOUD": "What floats in the sky and brings rain?",
            "DANCE": "What do you do to music at a party?",
            "EARTH": "What planet do we live on?",
            "FUNNY": "What word describes something that makes you laugh?",
            "GLASS": "What transparent material do windows use?",
            "HEART": "What organ pumps blood in your body?",
            "IMAGE": "What word means a picture or photograph?",
            "JOKER": "Who is the funny character in a deck of cards?",
            "KNIFE": "What sharp tool do you use to cut food?",
            "LIGHT": "What makes things visible and bright?",
            "MAGIC": "What word describes mysterious tricks and spells?",
            "NIGHT": "What time of day comes after evening?",
            "OCEAN": "What large body of salt water covers most of Earth?",
            "PIANO": "What musical instrument has black and white keys?",
            "QUICK": "What word means fast or speedy?",
            "RIVER": "What flows from mountains to the sea?",
            "SMILE": "What do you do when you're happy?",
            "TIGER": "What big cat has orange fur with black stripes?",
            "UNITY": "What word means togetherness or harmony?",
            "VALUE": "What word means worth or importance?",
            "WATER": "What clear liquid do you drink?",
            "YOUTH": "What word means the time when you're young?",
            "ZEBRA": "What black and white striped animal lives in Africa?",
            "BREAD": "What food do you make from flour and bake?",
            "CHAIR": "What furniture do you sit on?",
            "DREAM": "What do you see when you sleep?",
            "EAGLE": "What bird is a symbol of freedom and strength?",
            "FLAME": "What is the visible part of fire?",
            "GRACE": "What word means elegance or beauty in movement?",
            "HAPPY": "What word describes feeling joyful?",
            "IVORY": "What material comes from elephant tusks?",
            "JUMPS": "What action means to leap into the air?",
            "KNEEL": "What do you do when you bend down on one knee?",
            "LEMON": "What yellow sour fruit makes lemonade?",
            "MUSIC": "What art form uses sounds and melodies?",
            "NURSE": "Who takes care of patients in a hospital?",
            "OLIVE": "What small green fruit grows on trees?",
            "PEACE": "What word means calm and no war?",
            "QUEEN": "What is a female ruler called?",
            "ROBOT": "What mechanical being can do tasks automatically?",
            "SPACE": "What is the area beyond Earth's atmosphere?",
            "THREE": "What number comes after two?",
            "URBAN": "What word describes city areas?",
            "VIVID": "What word means bright and intense?",
            "WHEAT": "What grain is used to make bread?",
            "YACHT": "What is a luxury boat called?",
            "ZONES": "What word means areas or regions?",
            "GUESS": "What do you do when you try to figure something out?",
            "HOUSE": "What building do people live in?",
            "ROSES": "What red flowers are given on Valentine's Day?",
            "CATCH": "What do you do with a ball in baseball?",
            "WORLD": "What is the planet we live on called?",
            "WORDS": "What are letters combined together called?",
            "SEVEN": "What number comes after six?",
            "EIGHT": "What number comes after seven?",
            "WHERE": "What question word asks about location?",
            "WHICH": "What question word asks you to choose?",
            "WITCH": "What is a magical woman with a broomstick?",
            "MODEL": "What word means a representation or example?"
        }
        return questions
    
    def load_words(self) -> List[str]:
        """Load five-letter words from the wordlist file."""
        words = []
        try:
            with open(self.wordlist_file, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip().upper()
                    # Skip header lines and empty lines
                    if word and len(word) == 5 and word.isalpha():
                        # Skip if it's a header like "FIVE LETTER WORDS:"
                        if not word.startswith("FIVE") and not word.startswith("LETTER"):
                            words.append(word)
            
            if not words:
                # Fallback word list if file is empty
                words = ["APPLE", "BEACH", "BRAVE", "CLOUD", "DANCE", "EARTH", 
                        "FUNNY", "GLASS", "HEART", "IMAGE", "JOKER", "KNIFE",
                        "LIGHT", "MAGIC", "NIGHT", "OCEAN", "PIANO", "QUICK",
                        "RIVER", "SMILE", "TIGER", "UNITY", "VALUE", "WATER"]
            
            return words
        except FileNotFoundError:
            print(f"Warning: {self.wordlist_file} not found. Using default word list.")
            return ["APPLE", "BEACH", "BRAVE", "CLOUD", "DANCE", "EARTH", 
                   "FUNNY", "GLASS", "HEART", "IMAGE", "JOKER", "KNIFE",
                   "LIGHT", "MAGIC", "NIGHT", "OCEAN", "PIANO", "QUICK",
                   "RIVER", "SMILE", "TIGER", "UNITY", "VALUE", "WATER"]
    
    def start_new_game(self):
        """Start a new game with a random word and its question."""
        if not self.words:
            print("Error: No words available in wordlist!")
            return False
        
        self.secret_word = random.choice(self.words).upper()
        # Get the question for this word, or use a default if not found
        self.current_question = self.questions.get(self.secret_word, 
                                                   f"Guess the 5-letter word!")
        self.attempts = []
        return True
    
    def check_guess(self, guess: str) -> List[Tuple[str, str]]:
        """
        Check the guess against the secret word.
        Returns a list of tuples: (letter, status)
        Status: 'correct' (green), 'present' (yellow), 'absent' (gray)
        """
        guess = guess.upper()
        result = []
        secret_list = list(self.secret_word)
        guess_list = list(guess)
        
        # First pass: mark correct positions
        for i in range(5):
            if guess_list[i] == secret_list[i]:
                result.append((guess_list[i], 'correct'))
                secret_list[i] = None  # Mark as used
                guess_list[i] = None
            else:
                result.append((guess[i], None))
        
        # Second pass: mark present but wrong position
        for i in range(5):
            if result[i][1] is None:  # Not already marked as correct
                letter = guess[i]
                if letter in secret_list:
                    result[i] = (letter, 'present')
                    secret_list[secret_list.index(letter)] = None  # Mark as used
                else:
                    result[i] = (letter, 'absent')
        
        return result
    
    def is_valid_guess(self, guess: str) -> bool:
        """Check if the guess is valid (5 letters, alphabetic)."""
        guess = guess.strip().upper()
        if len(guess) != 5:
            return False
        if not guess.isalpha():
            return False
        return True
    
    def display_guess_result(self, result: List[Tuple[str, str]]):
        """Display the guess result with color coding."""
        # ANSI color codes
        GREEN = '\033[92m'  # Correct position
        YELLOW = '\033[93m'  # Present but wrong position
        GRAY = '\033[90m'    # Absent
        RESET = '\033[0m'    # Reset color
        
        colored_word = ""
        for letter, status in result:
            if status == 'correct':
                colored_word += f"{GREEN}{letter}{RESET} "
            elif status == 'present':
                colored_word += f"{YELLOW}{letter}{RESET} "
            else:
                colored_word += f"{GRAY}{letter}{RESET} "
        
        print(colored_word)
    
    def display_all_attempts(self):
        """Display all previous attempts."""
        print("\n" + "="*30)
        print("Your Guesses:")
        print("="*30)
        for attempt in self.attempts:
            self.display_guess_result(attempt)
        print("="*30 + "\n")
    
    def play(self):
        """Main game loop."""
        print("\n" + "="*50)
        print("🎮 WELCOME TO THE FIVE-LETTER WORD GUESSING GAME! 🎮")
        print("="*50)
        print(f"\nYou have {self.max_attempts} attempts to guess the word.")
        print("💚 Green = Correct letter in correct position")
        print("💛 Yellow = Letter exists but in wrong position")
        print("⚪ Gray = Letter not in the word")
        print("\n" + "-"*50 + "\n")
        
        if not self.start_new_game():
            return
        
        # Display the question
        print("❓ QUESTION:")
        print(f"   {self.current_question}")
        print(f"\n💡 Hint: The answer is a 5-letter word!")
        print("-"*50 + "\n")
        
        while len(self.attempts) < self.max_attempts:
            remaining = self.max_attempts - len(self.attempts)
            print(f"Attempts remaining: {remaining}")
            
            guess = input("Enter your 5-letter word guess: ").strip().upper()
            
            if not self.is_valid_guess(guess):
                print("❌ Invalid guess! Please enter exactly 5 letters.\n")
                continue
            
            result = self.check_guess(guess)
            self.attempts.append(result)
            
            # Clear screen for better display (optional)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Display question again
            print("\n" + "="*50)
            print("❓ QUESTION:")
            print(f"   {self.current_question}")
            print("="*50)
            
            self.display_all_attempts()
            
            # Check if player won
            if all(status == 'correct' for _, status in result):
                print("🎉🎉🎉 CONGRATULATIONS! YOU WON! 🎉🎉🎉")
                print(f"The answer was: {self.secret_word}")
                print(f"Question: {self.current_question}")
                return
            
            # Check if player lost
            if len(self.attempts) >= self.max_attempts:
                print("😢 Game Over! You ran out of attempts.")
                print(f"The answer was: {self.secret_word}")
                print(f"Question: {self.current_question}")
                return
        
        print("\nThanks for playing!")


def main():
    """Main function to run the game."""
    game = WordGuessGame()
    
    while True:
        game.play()
        
        play_again = input("\nWould you like to play again? (yes/no): ").strip().lower()
        if play_again not in ['yes', 'y']:
            print("Thanks for playing! Goodbye! 👋")
            break


if __name__ == "__main__":
    main()
