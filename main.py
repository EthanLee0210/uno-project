import deck_functions as df
import hand_functions as hf
import player_functions as pf


class Token:
    def __init__(self):
        self.count = 0
        self.last_card = ''
        self.wild_color = ''
        self.is_reversed = False
        self.is_first_reversed = False
        self.is_skipped = False
        self.is_draw_two = False
        self.is_draw_four = False
        self.skip_after_draw = False

    def __str__(self):
        return 'Player ' + str(len(players)) + ': ' + players[self.count].name + ' is up!'

    def increment(self):
        if not self.is_reversed:
            if self.count == len(players) - 1:
                self.count = 0
            else:
                self.count += 1
        else:
            if self.count == 0:
                self.count = len(players) - 1
            else:
                self.count -= 1

    def reverse(self):
        if self.is_reversed:
            self.is_reversed = False
        else:
            self.is_reversed = True

    def read_last(self):
        print('Last card played was a {}.'.format(hf.decode(self.last_card)))


# SETUP
players = [pf.Player(1, 'Dan'), pf.Player(2, 'Ethan'), pf.Player(3, 'Holton')]  # placeholder players
# players = pf.setup_players()  # actual player constructor
token = Token()
token.last_card = df.choose_card()
while token.last_card[0] == 'w' or token.last_card[1] == 'd' or token.last_card[1] == 's' or token.last_card[1] == 'r':
    token.last_card = df.choose_card()  # So that we don't start the game with a Wild/Skip/Draw/Reverse

# GAMEPLAY LOOP players[token.count] is how we refer to the player whose turn it is.
while True:
    if token.is_skipped:
        print(players[token.count].name + ', you\'re skipped this turn. Boo hoo, better luck next time!\n')
        token.is_skipped = False  # And then it skips all the rest of that player's actions.
    else:
        if token.is_first_reversed:  # Give a special greeting to the person right after the reverse.
            print('Back to you, {}!'.format(players[token.count].name))
            token.is_first_reversed = False  # Make it so it doesn't do that again.
        else:
            print('Player {}: {} you\'re up!'.format(token.count + 1, players[token.count].name))
        if token.is_draw_two:
            players[token.count].draw_two()
            token.is_draw_two = False
        elif token.is_draw_four:
            players[token.count].draw_four()
            token.is_draw_four = False
        else:
            players[token.count].holding()
        token.read_last()

        # ONE PLAYER'S TURN LOOP
        while True:
            print('What would you like to do?')
            print('  1. Draw a card\n  2. Play a card\n--> ', end='')
            prompt = input()
            if prompt == '1':  # Draw a card
                players[token.count].draw_card(read=True)
                players[token.count].holding(now=True)
                token.read_last()
            elif prompt == '2':  # Play a card
                choice = players[token.count].play_card()
                if choice == -1:
                    continue
                chosen_card = players[token.count].hand[choice]
                if not hf.is_legal(chosen_card, token.last_card):
                    hf.admonish(chosen_card, token.last_card)
                else:
                    print('You played: ' + hf.decode(chosen_card) + '.')
                    token.last_card = chosen_card
                    token.wild_color = ''  # Clear the restriction on what color can be played.
                    if chosen_card[0] == 'w':  # Record any actions that affect the following player. vv
                        print('What color do you choose?')
                        print('r = Red | y = Yellow | g = Green | b = Blue')
                        token.wild_color = input('  --> ')
                        token.last_card = token.wild_color + chosen_card[1]
                    if chosen_card[1] == 's':
                        token.is_skipped = True
                    elif chosen_card[1] == 'r':
                        token.reverse()
                        token.is_first_reversed = True
                    elif chosen_card[1] == 'd':
                        token.is_draw_two = True
                    elif chosen_card[1] == 'f':
                        token.is_draw_four = True
                    players[token.count].hand.remove(chosen_card)
                    players[token.count].holding(now=True)
                    ending = input('Type "end" to end your turn. --> ')
                    if ending.lower() == 'uno':
                        print(players[token.count].name + ' declares UNO! Watch out!')
                    print()
                    break
            elif prompt == 'd2':
                players[token.count].draw_two()
            elif prompt == 'done':  # End turn
                break
            elif prompt == 'exit':
                break
    if prompt == 'exit':
        break
    token.increment()
