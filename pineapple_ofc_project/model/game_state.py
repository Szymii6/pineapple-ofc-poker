# model/game_state.py

class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        """Resetuje wszystkie dane stanu gry."""
        self.deck = []
        self.top = []
        self.middle = []
        self.bottom = []
        self.hand = []

    def get_slot(self, slot_name):
        """Zwraca listę kart w danym slocie ('top', 'middle', 'bottom')."""
        return getattr(self, slot_name, [])

    def add_to_slot(self, slot_name, card):
        """Dodaje kartę do określonego slotu."""
        slot = self.get_slot(slot_name)
        slot.append(card)

    def remove_from_hand(self, card):
        """Usuwa kartę z ręki gracza."""
        if card in self.hand:
            self.hand.remove(card)
