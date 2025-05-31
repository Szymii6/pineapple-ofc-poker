from collections import Counter

# Stałe i słowniki rankingowe
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['♠', '♥', '♦', '♣']
RANK_ORDER = {rank: i for i, rank in enumerate(RANKS)}

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.name = rank + suit  # np. "10♠"

    def __repr__(self):
        return self.name

def hand_strength(cards):
    if len(cards) < 3:
        return 0, [0], "Brak układu"

    values = sorted([RANK_ORDER[c.rank] for c in cards], reverse=True)
    suits = [c.suit for c in cards]
    counts = Counter(values)

    is_flush = len(set(suits)) == 1 and len(cards) >= 5
    is_straight = (
        len(set(values)) >= 5 and
        all(values[i] - 1 == values[i + 1] for i in range(len(values) - 1)) and
        len(cards) >= 5
    )

    if is_straight and is_flush:
        return 8, values, "Poker"
    if 4 in counts.values():
        quad = max(k for k, v in counts.items() if v == 4)
        kickers = sorted([k for k in values if k != quad], reverse=True)
        return 7, [quad] + kickers, "Kareta"
    if 3 in counts.values() and 2 in counts.values():
        trips = max(k for k, v in counts.items() if v == 3)
        pair = max(k for k, v in counts.items() if v == 2)
        return 6, [trips, pair], "Full"
    if is_flush:
        return 5, values, "Kolor"
    if is_straight:
        return 4, values, "Strit"
    if 3 in counts.values():
        trips = max(k for k, v in counts.items() if v == 3)
        kickers = sorted([k for k in values if k != trips], reverse=True)
        return 3, [trips] + kickers, "Trójka"
    if list(counts.values()).count(2) >= 2:
        pairs = sorted([k for k, v in counts.items() if v == 2], reverse=True)
        kicker = max([k for k in values if k not in pairs])
        return 2, pairs + [kicker], "Dwie pary"
    if 2 in counts.values():
        pair = max(k for k, v in counts.items() if v == 2)
        kickers = sorted([k for k in values if k != pair], reverse=True)
        return 1, [pair] + kickers, "Para"

    return 0, values, "Wysoka karta"

