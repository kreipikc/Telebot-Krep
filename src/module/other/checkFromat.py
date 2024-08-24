def check(stavka, balance):
    try:
        s = int(stavka)
        b = int(balance)
        return True
    except:
        return False