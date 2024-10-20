#!/usr/bin/env python3

"""This program plays a game of Rock, Paper, Scissors between a human player
and a computer, and reports both players' scores each round, while logging
results to a file."""

import random
from datetime import datetime

# Possible moves in the game
moves = ['rock', 'paper', 'scissors']


class Player:
    """The Player class is the parent class for all of the Players
    in this game."""

    def __init__(self, name="Player"):
        self.name = name

    def move(self):
        return 'rock'

    def learn(self, my_move, their_move):
        pass


class Human(Player):
    """Human player that prompts the user to make a move."""

    def move(self):
        move = input(f"{self.name}, enter your move (rock, paper, scissors): "
                     ).lower()
        while move not in moves:
            move = input("Invalid move. Please try again "
                         "(rock, paper, scissors): ").lower()
        return move


class RockPlayer(Player):
    """Computer player that always plays 'rock'."""

    def move(self):
        return 'rock'


class RandomPlayer(Player):
    """Computer player that chooses a random move."""

    def move(self):
        return random.choice(moves)


class ReflectPlayer(Player):
    """Computer player that mimics the opponent's last move."""

    def __init__(self, name="Player"):
        super().__init__(name)
        self.opponent_last_move = None

    def move(self):
        if self.opponent_last_move:
            return self.opponent_last_move
        else:
            return random.choice(moves)

    def learn(self, my_move, their_move):
        self.opponent_last_move = their_move


class CyclePlayer(Player):
    """Computer player that cycles through the three moves."""

    def __init__(self, name="Player"):
        super().__init__(name)
        self.index = 0

    def move(self):
        move = moves[self.index]
        self.index = (self.index + 1) % len(moves)
        return move


def beats(one, two):
    """Determines if one move beats the other."""
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


class Game:
    """Handles the game logic, scoring, and logging."""

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.score1 = 0
        self.score2 = 0
        # Create a log file with the current date and time in the format
        # yyyyMMddhhmmss-game.log
        self.log_file_name = datetime.now().strftime('%Y%m%d%H%M%S')
        self.log_file_name = self.log_file_name + '-game.log'

    def log_result(self, message):
        """Logs the game result to the log file."""
        with open(self.log_file_name, 'a') as log_file:
            log_file.write(message + '\n')

    def play_round(self):
        """Plays a single round of the game."""
        move1 = self.p1.move()
        move2 = self.p2.move()
        print(f"{self.p1.name}: {move1}  {self.p2.name}: {move2}")

        if beats(move1, move2):
            self.score1 += 1
            result_message = f"{self.p1.name} wins this round!"
        elif beats(move2, move1):
            self.score2 += 1
            result_message = f"{self.p2.name} wins this round!"
        else:
            result_message = "It's a tie!"

        print(result_message)
        print(f"Scores: {self.p1.name} - {self.score1}, "
              f"{self.p2.name} - {self.score2}\n")

        # Log the result of the round
        self.log_result(f"{self.p1.name}: {move1}, {self.p2.name}: {move2} - "
                        f"{result_message}")

        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

    def play_game(self, rounds=3):
        """Plays the game for a specified number of rounds."""
        print("Game start!")
        self.log_result("Game start!")
        for round in range(rounds):
            print(f"Round {round + 1}:")
            self.log_result(f"Round {round + 1}:")
            self.play_round()
        print("Game over!")
        print(f"Final scores: {self.p1.name} - {self.score1}, "
              f"{self.p2.name} - {self.score2}")
        self.log_result("Game over!")
        self.log_result(f"Final scores: {self.p1.name} - {self.score1}, "
                        f"{self.p2.name} - {self.score2}")


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
