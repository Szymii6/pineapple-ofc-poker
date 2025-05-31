# controller/game_controller.py

from model.game_state import GameState
from model.card import Card, RANK_ORDER, hand_strength
import random

class GameController:
    def __init__(self, game_state):
        self.game_state = game_state
        self.view = None  # Przypisywana później przez set_view
        self.turn = 1
        self.selected_this_turn = 0
        self.hand_sprites = []

    def set_view(self, view):
        self.view = view
        self.draw_initial_hand()

    def draw_initial_hand(self):
        self.game_state.deck = [Card(rank, suit) for suit in ['♠', '♥', '♦', '♣'] for rank in RANK_ORDER]
        random.shuffle(self.game_state.deck)
        self.turn = 1
        self.selected_this_turn = 0
        self.game_state.top = []
        self.game_state.middle = []
        self.game_state.bottom = []
        self.game_state.hand = self.draw_cards(5)
        self.view.display_hand(self.game_state.hand)

    def reset_game(self):
        self.draw_initial_hand()

    def draw_cards(self, n):
        return [self.game_state.deck.pop() for _ in range(min(n, len(self.game_state.deck)))]

    def place_card(self, card, slot):
        if slot == 'top' and len(self.game_state.top) >= 3:
            return False
        if slot in ['middle', 'bottom'] and len(getattr(self.game_state, slot)) >= 5:
            return False

        max_cards = 5 if self.turn == 1 else 2
        if self.selected_this_turn >= max_cards:
            return False

        getattr(self.game_state, slot).append(card)
        self.game_state.hand.remove(card)
        self.selected_this_turn += 1

        if (self.turn == 1 and self.selected_this_turn == 5) or (self.turn > 1 and self.selected_this_turn == 2):
            self.next_turn()

        return True

    def next_turn(self):
        self.selected_this_turn = 0
        if self.turn >= 5:
            self.end_game()
        else:
            self.turn += 1
            self.game_state.hand = self.draw_cards(3)
            self.view.display_hand(self.game_state.hand)

    def end_game(self):
        top_val, top_tie, _ = hand_strength(self.game_state.top)
        mid_val, mid_tie, _ = hand_strength(self.game_state.middle)
        bot_val, bot_tie, _ = hand_strength(self.game_state.bottom)

        def is_stronger(rank1, tie1, rank2, tie2):
            if rank1 > rank2:
                return True
            elif rank1 == rank2:
                return tie1 > tie2
            return False

        folded = False
        if is_stronger(top_val, top_tie, mid_val, mid_tie) or is_stronger(mid_val, mid_tie, bot_val, bot_tie):
            folded = True

        result = []
        if folded:
            result.append("SPALONA RĘKA!")
        else:
            score_total = 0
            for name, multiplier in [('bottom', 1), ('middle', 2), ('top', 3)]:
                val, _, label = hand_strength(getattr(self.game_state, name))
                score = val * multiplier
                result.append(f"{name.upper()}: {val} ×{multiplier} = {score} ({label})")
                score_total += score
            result.append(f"Suma punktów: {score_total}")

        self.view.display_results(result)

