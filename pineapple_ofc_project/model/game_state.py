from patterns.singleton import SingletonMeta

class GameState(metaclass=SingletonMeta):
    def __init__(self):
        self.reset()

    def reset(self):
        self.deck = []
        self.top = []
        self.middle = []
        self.bottom = []
        self.hand = []

    def get_slot(self, slot_name):
        return getattr(self, slot_name, [])

    def add_to_slot(self, slot_name, card): 
        slot = self.get_slot(slot_name)
        slot.append(card)

    def remove_from_hand(self, card):
        if card in self.hand:
            self.hand.remove(card)