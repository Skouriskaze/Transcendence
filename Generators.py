import random
import Cards
import Transcendence

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
        cards = list(probabilities.keys())
        chosen_card = (
            random.choices(cards, [probabilities[card] for card in cards]))
        return chosen_card[0]()

class TileGenerator:
    @classmethod
    def get_random_tile(cls) -> 'Transcendence.Tile':
        probabilities = {
            Transcendence.Tile.ENHANCEMENT: 160,
            Transcendence.Tile.ADDITION: 235,
            Transcendence.Tile.CLONE: 160,
            Transcendence.Tile.RELOCATION: 170,
            Transcendence.Tile.MYSTERY: 160,
            Transcendence.Tile.BLESSING: 115,
        }
        tiles = list(probabilities.keys())
        chosen_tile = (
            random.choices(tiles, [probabilities[tile] for tile in tiles]))
        return chosen_tile[0]