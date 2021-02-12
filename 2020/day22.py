"""AdventOfCode Day22."""
import collections
from typing import List

test_input_1 = """\
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10\
"""

test_input_2 = """\
Player 1:
43
19

Player 2:
2
29
14
"""


def get_input():
    """Get puzzle input."""
    with open("input/day22.txt") as f:
        return f.read()


def preprocess(puzzle_input: str):
    players = puzzle_input.split("\n\n")
    player_a = [int(i) for i in players[0].split(":")[1].strip().splitlines()]
    player_b = [int(i) for i in players[1].split(":")[1].strip().splitlines()]
    return player_a, player_b


def playing(
    player_a,
    player_b: List[int],
    part2: bool = False,
    is_sub_game: bool = False,
):
    """Playing."""
    max_size = len(player_a) + len(player_b)

    queue_a = collections.deque(player_a, maxlen=max_size)
    queue_b = collections.deque(player_b, maxlen=max_size)

    prevention_rounds = set()
    round = 1
    while True:
        decks = (tuple(queue_a), tuple(queue_b))
        if decks in prevention_rounds:
            return "a", []
        prevention_rounds.add(decks)

        card_a = queue_a.popleft()
        card_b = queue_b.popleft()

        if part2 and card_a <= len(queue_a) and card_b <= len(queue_b):
            sub_player_a = list(queue_a)[:card_a]
            sub_player_b = list(queue_b)[:card_b]
            winner, _ = playing(
                sub_player_a,
                sub_player_b,
                True,
            )
            if winner == "a":
                queue_a.append(card_a)
                queue_a.append(card_b)
            else:
                queue_b.append(card_b)
                queue_b.append(card_a)
        elif card_a > card_b:
            queue_a.append(card_a)
            queue_a.append(card_b)
        else:
            queue_b.append(card_b)
            queue_b.append(card_a)
        if len(queue_a) == 0 or len(queue_b) == 0:
            break
        round += 1

    winner = "a" if len(queue_a) != 0 else "b"
    q = queue_a if len(queue_a) != 0 else queue_b
    cards = []
    for card in q:
        cards.append(card)
    return winner, cards


def part1(puzzle_input: str):
    """Part1."""
    player_a, player_b = preprocess(puzzle_input)
    _, cards = playing(player_a, player_b)

    score = 0
    for i, card in enumerate(cards):
        score += card * (len(cards) - i)
    return score


def part2(puzzle_input: str):
    """Part2."""
    player_a, player_b = preprocess(puzzle_input)
    winner, cards = playing(player_a, player_b, True)
    score = 0
    for i, card in enumerate(cards):
        score += card * (len(cards) - i)
    return score


if __name__ == "__main__":
    assert part1(test_input_1) == 306
    print(f"Part1: {part1(get_input())}")
    part2(test_input_2)
    assert part2(test_input_1) == 291
    print(f"Part2: {part2(get_input())}")
