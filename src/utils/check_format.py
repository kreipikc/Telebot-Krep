def check(bet, balance):
    try:
        s = int(bet)
        b = int(balance)
        return True
    except ValueError:
        return False