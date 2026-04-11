class CardPack:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add_card(self, card):
        if len(self.cards) < 40:
            self.cards.append(card)
        else:
            print(f"Cannot add more cards to {self.name} pack.")

class Card:
    def __init__(self, title, categories):
        self.title = title
        self.categories = categories

    def __str__(self):
        return f'{self.title}: {self.categories}'

# Creating card packs
animals_pack = CardPack("Animals")
movies_pack = CardPack("Movies")
countries_pack = CardPack("Countries")
technology_pack = CardPack("Technology")

# Example function to create cards
import random

categories = ["Speed", "Strength", "Intelligence", "Defense", "Agility"]

for _ in range(40):
    animals_pack.add_card(Card(f"Animal {random.randint(1, 100)}", {cat: random.randint(1, 10) for cat in categories}))
    movies_pack.add_card(Card(f"Movie {random.randint(1, 100)}", {cat: random.randint(1, 10) for cat in categories}))
    countries_pack.add_card(Card(f"Country {random.randint(1, 100)}", {cat: random.randint(1, 10) for cat in categories}))
    technology_pack.add_card(Card(f"Tech {random.randint(1, 100)}", {cat: random.randint(1, 10) for cat in categories}))

# Displaying the packs - Just for visual checking
for pack in [animals_pack, movies_pack, countries_pack, technology_pack]:
    print(f'\nContents of {pack.name} pack:')
    for card in pack.cards:
        print(card)