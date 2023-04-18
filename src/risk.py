import sys


def main():
    attackers = int(sys.argv[1])
    defenders = int(sys.argv[2])
    maxDice = max(200, attackers, defenders)
    expectedSurvivorsArray = [[None]*maxDice for x in range(maxDice)]
    likelihoodOfVictoryArray = [[None]*maxDice for x in range(maxDice)]

    readData("expectedSurvivors.txt", expectedSurvivorsArray)
    readData("likelihoodOfVictory.txt", likelihoodOfVictoryArray)
    print(
        "likelihood of victory "
        + str(round(likelihoodOfVictory(attackers, defenders) * 100, 1))
        + "% with "
        + str(round(expectedSurvivors(attackers, defenders), 2))
        + " survivors on average")
    writeData("expectedSurvivors.txt", expectedSurvivorsArray)
    writeData("likelihoodOfVictory.txt", likelihoodOfVictoryArray)


### Functions for the calculation ###

def expectedSurvivors(attackers: int, defenders: int, expectedSurvivorsArray):
    return recursiveMarkovChain(
        attackers,
        defenders,
        expectedSurvivorsArray,
        # if there are no defenders then all attackers survive
        lambda attackers: attackers if attackers > 0 else 0
    )


def likelihoodOfVictory(attackers: int, defenders: int, likelihoodOfVictoryArray):
    return recursiveMarkovChain(
        attackers,
        defenders,
        likelihoodOfVictoryArray,
        # if there are no defenders and any attackers they win with probability 1
        lambda attackers: 1 if attackers > 0 else 0
    )


def recursiveMarkovChain(attackers: int, defenders: int, memoryArray, baseCase):
    if (defenders <= 0 or attackers <= 0):
        return baseCase(attackers)

    rememberedValue = memoryArray[attackers-1][defenders-1]
    if (rememberedValue != None):
        return rememberedValue

    attackDie = min(attackers, 3)
    defenseDie = min(defenders, 2)

    # expected value of the chain(a,d) = \sum_l P(l)*chain(a-l, d - dd + l)
    result = sum(
        [
            # the probability of losses
            probabilityOfXLosses(attackDie, defenseDie, losses)
            # the expected value of the scenario after losses
            * recursiveMarkovChain(attackers - losses, defenders - defenseDie + losses, memoryArray, baseCase)
            for losses in range(min(attackDie, defenseDie) + 1)
        ]
    )

    memoryArray[attackers-1][defenders-1] = result
    return result


def probabilityOfXLosses(attackDie: int, defenseDie: int, losses: int):
    if (defenseDie == 0):
        return 0
    if (defenseDie == 1):
        return probabilityOfXLossesOneDefender(attackDie, losses)
    return probabilityOfXLossesTwoDefenders(attackDie, losses)


def probabilityOfXLossesOneDefender(attackDie: int, losses: int):
    if (losses == 0):
        return [0.417, 0.579, 0.66][attackDie - 1]
    return [0.583, 0.421, 0.34][attackDie - 1]


def probabilityOfXLossesTwoDefenders(attackDie: int, losses: int):
    if (losses == 0):
        return [0.255, 0.228, 0.372][attackDie - 1]
    if (losses == 1):
        return [0, 0.448, 0.292][attackDie - 1]
    return [0.745, 0.448, 0.336][attackDie - 1]


### Functions for reading and writing data ###

def readData(fileName: str, array):
    touch("./data/" + fileName)
    file = open("./data/" + fileName, "r")
    lines = file.readlines()
    file.close()

    readArray = [
        [n for n in l.split(",")] for l in lines
    ]

    rows = range(min(len(readArray), len(array)))

    for rowNum in rows:
        for colNum in rows:
            readVal = readArray[rowNum][colNum]
            if (readVal == "None" or readVal == "None\n"):
                readVal = None
            else:
                readVal = float(readVal)
            array[rowNum][colNum] = readVal


def touch(fileName: str):
    file = open(fileName, "a+")
    file.close()


def writeData(fileName: str, array):
    file = open("./data/" + fileName, "w")
    for row in array:
        file.write(",".join([str(x) for x in row])+"\n")
    file.close()


### Do it ###

main()
