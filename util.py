import random
import variables

rand = random.Random()

def log(message: str):
    if message == "":
        print("")
        return

    color = "\033[0m"

    if message.startswith("Info"):
        color = "\033[94m"
        pass
    elif message.startswith("Warning"):
        color = "\033[93m"
        pass
    elif message.startswith("Error"):
        color = "\033[91m"
        pass
    pass

    name = "[ " + variables.projectNameShort + " ]"
    print(color + name + ": " + message)
pass


def getRandomNumber(min: int, max: int):
    return rand.randint(min, max)
pass