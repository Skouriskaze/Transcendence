import random
import Cards

class CardGenerator:
    @classmethod
    def get_random_card(cls) -> Cards.Card:
        probabilities = {
            Cards.Thunder: 150,
            Cards.Hellfire: 115,
            Cards.Shockwave: 95,
            Cards.TidalWave: 55,
            Cards.Explosion: 105,
            Cards.Tempest: 70,
            Cards.Lightning: 90,
            Cards.Earthquake: 70,
            Cards.Purify: 100,
            Cards.Tornado: 150,
        }
        cards = list(probabilities.values())
        chosen_card = (
            random.choices(cards, [probabilities[card] for card in cards]))
        return chosen_card()