import random

def game_rulette_casino():
    list_black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    number = random.randint(0, 36)
    color = ''
    if number == 0:
        color = '🟢'
    elif number in list_black:
        color = '⚫'
    else:
        color = '🔴'
    return number, color