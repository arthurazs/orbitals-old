from game import Orbitals, Player

game = Orbitals(3, starting_seed=13)

arthur = Player('arthur')
game.add_player(arthur, Orbitals.RED)

lucas = Player('lucas')
game.add_player(lucas, Orbitals.GREEN)

noah = Player('noah')
game.add_player(noah, Orbitals.BLUE)

players = [None, arthur, lucas, noah]

order = game.start()
print(order)


player = arthur
_, name, colour = player.get_info()
game.paint(player, 1, 1, colour)


player = lucas
_, name, colour = player.get_info()
game.paint(player, 1, 1, colour)


player = noah
_, name, colour = player.get_info()
game.paint(player, 1, 1, colour)


extra_turn, last_turn = game.next_turn()
print(f'is there an extra turn? {extra_turn if extra_turn else "no"}')
print(f'was this the last turn? {"yes" if last_turn else "no"}')


player = arthur
_, name, colour = player.get_info()
game.paint(player, 0, 0, colour)


player = lucas
_, name, colour = player.get_info()
game.paint(player, 2, 2, colour)


player = noah
_, name, colour = player.get_info()
colour = Orbitals.GREEN
game.paint(player, 2, 2, colour)


extra_turn, last_turn = game.next_turn()
print(f'is there an extra turn? {extra_turn if extra_turn else "no"}')
print(f'was this the last turn? {"yes" if last_turn else "no"}')


player = noah
_, name, colour = player.get_info()
game.paint(player, 0, 0, colour)


last_turn = game.extra_turn()
print(f'was this the last turn? {"yes" if last_turn else "no"}')


player = arthur
_, name, colour = player.get_info()
colour = Orbitals.BLUE
game.paint(player, 0, 1, colour)


player = lucas
_, name, colour = player.get_info()
game.paint(player, 1, 0, colour)


player = noah
_, name, colour = player.get_info()
game.paint(player, 0, 1, colour)


extra_turn, last_turn = game.next_turn()
print(f'is there an extra turn? {extra_turn if extra_turn else "no"}')
print(f'was this the last turn? {"yes" if last_turn else "no"}')


player = arthur
_, name, colour = player.get_info()
game.paint(player, 2, 1, colour)


last_turn = game.extra_turn()
print(f'was this the last turn? {"yes" if last_turn else "no"}')

# <->


player = arthur
_, name, colour = player.get_info()
game.paint(player, 1, 1, colour)


player = lucas
_, name, colour = player.get_info()
game.paint(player, 1, 1, colour)


player = noah
_, name, colour = player.get_info()
game.paint(player, 1, 1, colour)


extra_turn, last_turn = game.next_turn()
print(f'is there an extra turn? {extra_turn if extra_turn else "no"}')
print(f'was this the last turn? {"yes" if last_turn else "no"}')


player = arthur
_, name, colour = player.get_info()
game.paint(player, 1, 1, colour)


player = lucas
_, name, colour = player.get_info()
game.paint(player, 1, 1, colour)


player = noah
_, name, colour = player.get_info()
game.paint(player, 1, 1, colour)


extra_turn, last_turn = game.next_turn()
print(f'is there an extra turn? {extra_turn if extra_turn else "no"}')
print(f'was this the last turn? {"yes" if last_turn else "no"}')

player = arthur
_, name, colour = player.get_info()
game.paint(player, 1, 1, colour)


player = lucas
_, name, colour = player.get_info()
game.paint(player, 1, 1, colour)


player = noah
_, name, colour = player.get_info()
game.paint(player, 1, 1, colour)


extra_turn, last_turn = game.next_turn()
print(f'is there an extra turn? {extra_turn if extra_turn else "no"}')
print(f'was this the last turn? {"yes" if last_turn else "no"}')

player = arthur
_, name, colour = player.get_info()
game.paint(player, 1, 1, colour)


player = lucas
_, name, colour = player.get_info()
game.paint(player, 1, 1, colour)


player = noah
_, name, colour = player.get_info()
game.paint(player, 1, 1, colour)


extra_turn, last_turn = game.next_turn()
print(f'is there an extra turn? {extra_turn if extra_turn else "no"}')
print(f'was this the last turn? {"yes" if last_turn else "no"}')

player = arthur
_, name, colour = player.get_info()
game.paint(player, 1, 1, colour)


player = lucas
_, name, colour = player.get_info()
game.paint(player, 1, 1, colour)


player = noah
_, name, colour = player.get_info()
game.paint(player, 1, 1, colour)


extra_turn, last_turn = game.next_turn()
print(f'is there an extra turn? {extra_turn if extra_turn else "no"}')
print(f'was this the last turn? {"yes" if last_turn else "no"}')


player = arthur
_, name, colour = player.get_info()
game.paint(player, 2, 2, colour)


player = lucas
_, name, colour = player.get_info()
game.paint(player, 1, 1, colour)


player = noah
_, name, colour = player.get_info()
game.paint(player, 2, 2, colour)

extra_turn, last_turn = game.next_turn()
print(f'is there an extra turn? {extra_turn if extra_turn else "no"}')
print(f'was this the last turn? {"yes" if last_turn else "no"}')


player = arthur
_, name, colour = player.get_info()
game.paint(player, 2, 2, colour)


player = lucas
_, name, colour = player.get_info()
game.paint(player, 1, 1, colour)


player = noah
_, name, colour = player.get_info()
game.paint(player, 2, 2, Orbitals.RED)

extra_turn, last_turn = game.next_turn()
print(f'is there an extra turn? {extra_turn if extra_turn else "no"}')
print(f'was this the last turn? {"yes" if last_turn else "no"}')

player = arthur
_, name, colour = player.get_info()
game.paint(player, 2, 2, Orbitals.GREEN)

last_turn = game.extra_turn()
print(f'was this the last turn? {"yes" if last_turn else "no"}')

winner = game.end()
print(players[winner].get_name())
