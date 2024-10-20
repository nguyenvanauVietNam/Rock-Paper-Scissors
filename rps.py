#!/usr/bin/env python3

"""This program plays a game of Rock, Paper, Scissors between a human player
and a computer, reports both players' scores each round, and logs
results to a file."""

import random
from datetime import datetime

# Possible moves in the game
MOVES = ['rock', 'paper', 'scissors']


class Player:
    """The Player class is the parent class for all players in the game."""

    def __init__(self, name="Player"):
        self.name = name  # Player's name

    def move(self):
        """Returns a default move."""
        return 'rock'

    def learn(self, my_move, their_move):
        """Method for learning opponent's move. To be implemented in subclasses."""
        pass


class Human(Player):
    """Human player that prompts the user to make a move."""

    def move(self):
        # Prompt the human player to enter their move
        player_move = input(f"{self.name}, Input your choice (rock, paper, scissors): ").lower()
        # Validate the player's input
        while player_move not in MOVES:
            print("Invalid move. Game over.")
            return None  # Return None if input is invalid
        return player_move  # Return the validated move


class RockPlayer(Player):
    """Computer player that always plays 'rock'."""

    def move(self):
        return 'rock'  # Always returns 'rock'


class RandomPlayer(Player):
    """Computer player that chooses a random move."""

    def move(self):
        return random.choice(MOVES)  # Returns a random move from the list


class ReflectPlayer(Player):
    """Computer player that mimics the opponent's last move."""

    def __init__(self, name="Player"):
        super().__init__(name)
        self.opponent_last_move = None  # Track the opponent's last move

    def move(self):
        # If the opponent's last move is known, mimic it; otherwise choose randomly
        if self.opponent_last_move:
            return self.opponent_last_move
        else:
            return random.choice(MOVES)

    def learn(self, my_move, their_move):
        """Store the opponent's last move."""
        self.opponent_last_move = their_move


class CyclePlayer(Player):
    """Computer player that cycles through the three moves."""

    def __init__(self, name="Player"):
        super().__init__(name)
        self.index = 0  # Start index for cycling through moves

    def move(self):
        # Get the current move based on the index and update the index for the next move
        move = MOVES[self.index]
        self.index = (self.index + 1) % len(MOVES)  # Cycle through moves
        return move


def beats(one, two):
    """Determines if one move beats the other."""
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


class Game:
    """Handles the game logic, scoring, and logging."""

    def __init__(self, player1, player2):
        self.player1 = player1  # The human player
        self.player2 = player2  # The computer player
        self.score1 = 0  # Score for player 1
        self.score2 = 0  # Score for player 2
        # Create a log file with the current date and time in the format yyyyMMddhhmmss-game.log
        self.log_file_name = datetime.now().strftime('%Y%m%d%H%M%S') + '-game.log'

    def log_result(self, message):
        """Logs the game result to the log file."""
        with open(self.log_file_name, 'a') as log_file:
            log_file.write(message + '\n')

    def play_round(self):
        """Plays a single round of the game."""
        move1 = self.player1.move()  # Get move from player 1
        if move1 is None:  # Check if the player's move is valid
            print("Game over.")
            return False  # End the game if the move is invalid

        move2 = self.player2.move()  # Get move from player 2
        print(f"{self.player1.name}: {move1}  {self.player2.name}: {move2}")

        # Determine the round's winner
        if beats(move1, move2):
            self.score1 += 1  # Increment score for player 1
            result_message = f"{self.player1.name} wins this round!"
        elif beats(move2, move1):
            self.score2 += 1  # Increment score for player 2
            result_message = f"{self.player2.name} wins this round!"
        else:
            result_message = "It's a tie!"  # Handle tie case

        print(f"{result_message} | Scores: {self.player1.name} - {self.score1}, {self.player2.name} - {self.score2}\n")

        # Log the result of the round
        self.log_result(f"{self.player1.name}: {move1}, {self.player2.name}: {move2} - {result_message}")

        self.player1.learn(move1, move2)  # Update player 1's knowledge
        self.player2.learn(move2, move1)  # Update player 2's knowledge

        return True  # Continue the game

    def play_game(self, rounds=3):
        """Plays the game for a specified number of rounds."""
        print("Game start!")
        self.log_result("Game start!")
        for round_number in range(rounds):
            print(f"Round {round_number + 1}:")
            self.log_result(f"Round {round_number + 1}:")
            if not self.play_round():  # Play a round
                break  # Exit if the game ended due to invalid input

        # Final results
        print("Game over!")
        print(f"Final scores: {self.player1.name} - {self.score1}, {self.player2.name} - {self.score2}")

        # Print final results based on scores
        if self.score1 > self.score2:
            print("You win!")  # Player 1 wins
            self.log_result("You win!")
        else:
            print("Game over, You lose.")  # Player 2 wins
            self.log_result("Game over, You lose.")

        self.log_result("Game over!")
        self.log_result(f"Final scores: {self.player1.name} - {self.score1}, "
                        f"{self.player2.name} - {self.score2}")


if __name__ == '__main__':
    # Get player name
    player1_name = input("Enter your name: ")

    # Create human player
    player1 = Human(player1_name)

    # Randomly select a computer player strategy
    computer_player = random.choice([
        RockPlayer("Computer"),
        RandomPlayer("Computer"),
        ReflectPlayer("Computer"),
        CyclePlayer("Computer")
    ])

    # Create a game with the human player and the computer player
    game = Game(player1, computer_player)

    # Play the game
    game.play_game(3)
