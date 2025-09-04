import random
import time

def number_guessing_game():
    print("🎯 Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    
    # Set difficulty level
    while True:
        try:
            difficulty = input("Choose difficulty (easy/medium/hard): ").lower()
            if difficulty == "easy":
                attempts = 10
                break
            elif difficulty == "medium":
                attempts = 7
                break
            elif difficulty == "hard":
                attempts = 5
                break
            else:
                print("Please choose from easy, medium, or hard.")
        except:
            print("Invalid input. Please try again.")
    
    # Generate random number
    secret_number = random.randint(1, 100)
    guesses = []
    
    print(f"\nYou have {attempts} attempts to guess the number.")
    
    # Main game loop
    for attempt in range(1, attempts + 1):
        print(f"\nAttempt {attempt} of {attempts}")
        
        # Get user's guess
        while True:
            try:
                guess = int(input("Enter your guess (1-100): "))
                if 1 <= guess <= 100:
                    break
                else:
                    print("Please enter a number between 1 and 100.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        guesses.append(guess)
        
        # Check the guess
        if guess == secret_number:
            print(f"🎉 Congratulations! You guessed it in {attempt} attempts!")
            print(f"Your guesses: {guesses}")
            return
        
        # Give hints
        difference = abs(secret_number - guess)
        if attempt < attempts:  # Only give hints if not the last attempt
            if difference <= 5:
                print("🔥 Very hot!")
            elif difference <= 15:
                print("☀️ Hot!")
            elif difference <= 25:
                print("🌤 Warm")
            else:
                print("❄️ Cold")
            
            if guess < secret_number:
                print("📈 Try a higher number.")
            else:
                print("📉 Try a lower number.")
    
    # If all attempts are used
    print(f"\n💔 Game over! The number was {secret_number}.")
    print(f"Your guesses: {guesses}")

# Run the game
if __name__ == "__main__":
    number_guessing_game()
    
    # Ask if player wants to play again
    while True:
        play_again = input("\nWould you like to play again? (yes/no): ").lower()
        if play_again in ["yes", "y"]:
            number_guessing_game()
        elif play_again in ["no", "n"]:
            print("Thanks for playing! 👋")
            break
        else:
            print("Please enter yes or no.")