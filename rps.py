#!/usr/bin/env python3
"""This program plays a game of Rock, Paper, Scissors between a user player
and a bot player, reports both players' scores each round, and logs
results to a file.
Reference Document
https://www.cs.drexel.edu/~popyack/Courses/CSP/Fa17/notes/
CS140_RockPaperScissors_Revisited.pdf
"""

import random
from datetime import datetime

# Possible moves in the game
moves = ['rock', 'paper', 'scissors']


class Player:
    """The Player class is the parent class for all players in the game."""

    def __init__(self, name="Player"):
        self.name = name  # Player's name

    def move(self):
        """Returns a default move."""
        return 'rock'

    def learn(self, my_move, their_move):
        """Method for learning opponent's move.
        To be implemented in subclasses."""
        pass


class User_Player(Player):
    """User player that prompts the user to make a move."""

    def move(self):
        # User player chooses (rock, paper, scissors)
        try:
            user_move = input(
                f"{self.name}, Please choose (rock, paper, scissors) "
                "or 'exit' to quit: "
            ).lower()
            # Allow the user to exit the game
            if user_move == 'exit':
                return 'exit'
            # Validate the user's input
            while user_move not in moves:
                print("Invalid move. Please try again or type 'exit' to quit.")
                user_move = input(
                    f"{self.name}, Input your choice (rock, paper, scissors): "
                ).lower()  # User chooses again
                if user_move == 'exit':
                    return 'exit'
            return user_move  # Return the validated move
        except Exception as e:
            # Handle any unexpected exceptions during user input
            print(f"An error occurred: {e}. Exiting the game.")
            return 'exit'  # Returning 'exit'


class RockBot(Player):
    """Bot player that always plays 'rock'."""

    def move(self):
        return 'rock'  # Always returns 'rock'

    def learn(self, my_move, their_move):
        """RockBot doesn't need to learn, it always plays rock."""
        pass


class RandomBot(Player):
    """Bot player that chooses a random move."""

    def move(self):
        return random.choice(moves)  # Returns a random move from the list

    def learn(self, my_move, their_move):
        """RandomBot doesn't need to learn, it always plays randomly."""
        pass


class MimickingBot(Player):
    """Bot player that mimics the opponent's last move."""

    def __init__(self, name="Player"):
        super().__init__(name)
        self.opponent_last_move = None  # Track the opponent's last move

    def move(self):
        # If the opponent's last move is known,
        # mimic it; otherwise choose randomly
        if self.opponent_last_move:
            return self.opponent_last_move
        else:
            return random.choice(moves)

    def learn(self, my_move, their_move):
        """Store the opponent's last move."""
        self.opponent_last_move = their_move


class CyclingBot(Player):
    """Bot player that cycles through the three moves."""

    def __init__(self, name="Player"):
        super().__init__(name)
        self.next_move_index = 0  # Start index for cycling through moves

    def move(self):
        """Get the current move based on the index and update the index
        for the next move."""
        move = moves[self.next_move_index]  # Current move
        self.next_move_index = (self.next_move_index + 1) % len(moves)
        # Cycle through moves
        return move

    def learn(self, my_move, their_move):
        """Determine the next move based on my_move."""
        # Update the index based on the current move played
        if my_move == 'rock':
            self.next_move_index = 1  # Next move is 'paper'
        elif my_move == 'paper':
            self.next_move_index = 2  # Next move is 'scissors'
        elif my_move == 'scissors':
            self.next_move_index = 0  # Next move is 'rock'


def beats(one, two):
    """Determines if one move beats the other."""
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


class Game:
    """Handles the game logic, scoring, and logging."""

    def __init__(self, user_player, bot_player):
        self.user_player = user_player  # The user player
        self.bot_player = bot_player  # The bot player
        self.score_user = 0  # Score for user player
        self.score_bot = 0  # Score for bot player
        self.consecutive_wins_user = 0  # Track consecutive wins for user
        self.consecutive_wins_bot = 0  # Track consecutive wins for bot
        # Create a log file with the current date and time in the format
        # yyyyMMddHHmmss-game.log
        self.log_file_name = (
            datetime.now().strftime('%Y%m%d%H%M%S') + '-game.log'
        )

    def log_result(self, message):
        """Logs the game result to the log file."""
        try:
            with open(self.log_file_name, 'a') as log_file:
                log_file.write(message + '\n')
        except Exception as e:
            # Handle file write exceptions gracefully
            print(f"Failed to write to log file: {e}")

    def play_round(self):
        """Plays a single round of the game."""
        try:
            # Display the scores before each round
            print(f"\nCurrent Scores: {self.user_player.name} -"
                  f" {self.score_user}, "
                  f"{self.bot_player.name} - {self.score_bot}")
            print("Type 'exit' at any time to quit the game.")

            move_user = self.user_player.move()  # Get move from user player
            if move_user == 'exit':  # Check if the user wants to exit
                print("Exiting the game.")
                return False  # End the game if 'exit' is entered

            move_bot = self.bot_player.move()  # Get move from bot player
            print(f"{self.user_player.name}: {move_user} "
                  f"{self.bot_player.name}: {move_bot}")

            # Determine the round's winner and update scores
            if beats(move_user, move_bot):  # User wins the round
                self.score_user += 1
                self.score_bot = max(0, self.score_bot - 3)  # negative score
                self.consecutive_wins_user += 1
                self.consecutive_wins_bot = 0  # Reset bot's consecutive wins
                result_message = f"{self.user_player.name} wins this round!"
            elif beats(move_bot, move_user):  # Bot wins the round
                self.score_bot += 1
                self.score_user = max(0, self.score_user - 3)  # negative score
                self.consecutive_wins_bot += 1
                self.consecutive_wins_user = 0  # Reset user's consecutive wins
                result_message = f"{self.bot_player.name} wins this round!"
            else:
                # Handle tie case, no score changes
                self.consecutive_wins_user = 0  # Reset consecutive wins
                self.consecutive_wins_bot = 0
                result_message = "It's a tie!"

            print(f"{result_message} | Scores: {self.user_player.name} - "
                  f"{self.score_user}, "
                  f"{self.bot_player.name} - {self.score_bot}\n")

            # Log the result of the round
            self.log_result(
                f"{self.user_player.name}: {move_user}, "
                f"{self.bot_player.name}: {move_bot} - "
                f"{result_message}"
            )
            # Update user player's knowledge
            self.user_player.learn(move_user, move_bot)
            # Update bot player's knowledge
            self.bot_player.learn(move_bot, move_user)

            # Check if either player has won
            if self.score_user >= 3 or self.consecutive_wins_user == 3:
                print(f"{self.user_player.name} wins the game!")
                self.log_result(f"{self.user_player.name} wins the game!")
                return False  # End the game
            elif self.score_bot >= 3 or self.consecutive_wins_bot == 3:
                print(f"{self.bot_player.name} wins the game!")
                self.log_result(f"{self.bot_player.name} wins the game!")
                return False  # End the game

            return True  # Continue the game
        except Exception as e:
            # Handle unexpected exceptions during a round
            print(f"An error occurred during the round: {e}.")
            return False  # End the game gracefully

    def play_game(self):
        """Plays the game with the new rules."""
        try:
            print("Game start!")
            self.log_result("Game start!")
            while True:
                # Keep playing rounds until one player wins the game
                if not self.play_round():  # returns False, exit game
                    break
            print("Game over! Thank you for playing.")
        except Exception as e:
            # Handle unexpected exceptions during the game
            print(f"An error occurred: {e}. Exiting the game.")


# Start the game
if __name__ == '__main__':
    user_name = input("Enter your name: ")
    user_player = User_Player(user_name)  # Create user player with a name
    bot = RandomBot()  # You can change this to any bot type
    # Randomly select a bot player strategy
    bot_player = random.choice([
        RockBot("RockBot"),
        RandomBot("RandomBot"),
        MimickingBot("MimickingBot"),
        CyclingBot("CyclingBot")
    ])
    game = Game(user_player, bot_player)  # Initialize the game
    game.play_game()  # Start the game
