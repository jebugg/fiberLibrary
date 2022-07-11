import random

def getRandInt(start:int = 50, end:int = 1000):
    import random
    random.seed()
    return random.randint(start, end)

def getRandFloat(start:int = 0, end:int = 100):
    import random
    random.seed()
    return random.random()*(end-start) + start