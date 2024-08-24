import random

def random_from_val(mode: str) -> str:
    maps = ['sunset', 'lotus', 'pearl', 'fracture', 'breeze', 'icebox', 'bind', 'haven', 'split', 'ascent']
    agent = ['deadlock', 'iso', 'brimstone', 'phoenix', 'sage', 'sova', 'viper', 'cypher', 'reyna', 'killjoy', 'breach', 'omen', 'jett', 'raze', 'yoru', 'skye', 'astra', 'kayo', 'chamber', 'neon', 'fade', 'harbor', 'gekko', 'clove']
    guns = ['knife', 'classic', 'shorty', 'frenzy', 'ghost', 'sheriff', 'stinger', 'spectre', 'bucky', 'judge', 'bulldog', 'guardian', 'phantom', 'vandal', 'marshal', 'operator', 'ares', 'odin', 'outlaw']
    if mode == 'Карты':
        return random.choice(maps)
    elif mode == 'Агенты':
        return random.choice(agent)
    elif mode == 'Оружия':
        return random.choice(guns)
