from game import Orbitals, Player

game = Orbitals(3, starting_seed=13)

arthur = Player('arthur')
game.add_player(arthur, Orbitals.RED)

lucas = Player('lucas')
game.add_player(lucas, Orbitals.GREEN)

noah = Player('noah')
game.add_player(noah, Orbitals.BLUE)

players = [None, arthur, lucas, noah]

game.start()
for r in range(2):
    for c in range(3):
        player = players[c + 1]
        colour = player.get_colour()
        game.paint(player, c, r, colour)

    extra_turn, last_turn = game.next_turn()
    print(f'is there an extra turn? {extra_turn if extra_turn else "no"}')
    print(f'was this the last turn? {"yes" if last_turn else "no"}')

if False:
    game.paint(arthur, 0, 2, Orbitals.BLUE)
    game.paint(lucas, 1, 2, Orbitals.GREEN)
    game.paint(noah, 0, 2, Orbitals.BLUE)

    extra_turn, last_turn = game.next_turn()
    print(f'is there an extra turn? {extra_turn if extra_turn else "no"}')
    print(f'was this the last turn? {"yes" if last_turn else "no"}')

    game.paint(arthur, 0, 2, Orbitals.RED)

    last_turn = game.extra_turn()
    print(f'was this the last turn? {"yes" if last_turn else "no"}')
else:
    game.paint(arthur, 0, 2, Orbitals.RED)
    game.paint(lucas, 1, 2, Orbitals.GREEN)
    game.paint(noah, 2, 2, Orbitals.BLUE)

    extra_turn, last_turn = game.next_turn()
    print(f'is there an extra turn? {extra_turn if extra_turn else "no"}')
    print(f'was this the last turn? {"yes" if last_turn else "no"}')

    game.paint(arthur, 2, 2, Orbitals.BLUE)
    game.paint(lucas, 2, 2, Orbitals.GREEN)
    game.paint(noah, 2, 2, Orbitals.BLUE)

    extra_turn, last_turn = game.next_turn()
    print(f'is there an extra turn? {extra_turn if extra_turn else "no"}')
    print(f'was this the last turn? {"yes" if last_turn else "no"}')

    winner = game.end()
    print(f'{players[winner].get_name()} won')
