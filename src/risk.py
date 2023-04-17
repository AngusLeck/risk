import sys

attackers = int(sys.argv[1])
defenders = int(sys.argv[2])
maxDice = max(200, attackers, defenders)
expectedSurvivorsArray = [[None]*maxDice for x in range(maxDice)]
probabilityOfVictoryArray = [[None]*maxDice for x in range(maxDice)]


def main():
    readData("expectedSurvivors.txt", expectedSurvivorsArray)
    readData("likelihoodOfVictory.txt", probabilityOfVictoryArray)
    print(
        "likelihood of victory "
        + str(round(likelihoodOfVictory(attackers, defenders) * 100, 1))
        + "% with "
        + str(round(expectedSurvivors(attackers, defenders), 2))
        + " survivors on average")
    writeData("expectedSurvivors.txt", expectedSurvivorsArray)
    writeData("likelihoodOfVictory.txt", probabilityOfVictoryArray)


def expectedSurvivors(attackDie: int, defenseDie: int):
    if (attackDie <= 0):
        return 0
    if (defenseDie <= 0):
        return attackDie

    rememberedValue = expectedSurvivorsArray[attackDie-1][defenseDie-1]
    if (rememberedValue != None):
        return rememberedValue

    result = sum(
        [
            probabilityOfXLosses(min(attackDie, 3), min(defenseDie, 2), x)
            * expectedSurvivors(attackDie - x, defenseDie - min(defenseDie, 2) + x)
            for x in range(min(attackDie, defenseDie, 2) + 1)
        ]
    )
    expectedSurvivorsArray[attackDie-1][defenseDie-1] = result
    return result


def likelihoodOfVictory(attackDie: int, defenseDie: int):
    if (attackDie <= 0):
        return 0
    if (defenseDie <= 0):
        return 1

    rememberedValue = probabilityOfVictoryArray[attackDie-1][defenseDie-1]
    if (rememberedValue != None):
        return rememberedValue

    result = sum(
        [
            probabilityOfXLosses(min(attackDie, 3), min(defenseDie, 2), x)
            * likelihoodOfVictory(attackDie - x, defenseDie - min(defenseDie, 2) + x)
            for x in range(min(attackDie, defenseDie, 2) + 1)
        ]
    )
    probabilityOfVictoryArray[attackDie-1][defenseDie-1] = result
    return result


def readData(fileName: str, array):
    touch("./data/" + fileName)
    file = open("./data/" + fileName, "r")
    lines = file.readlines()
    file.close()

    readArray = [
        [n for n in l.split(",")] for l in lines
    ]

    rows = range(min(len(readArray), maxDice))

    for rowNum in rows:
        for colNum in rows:
            readVal = readArray[rowNum][colNum]
            if (readVal == "None" or readVal == "None\n"):
                readVal = None
            else:
                readVal = float(readVal)
            array[rowNum][colNum] = readVal


def touch(fileName: str):
    file = open(fileName, "w+")
    file.close()


def writeData(fileName: str, array):
    file = open("./data/" + fileName, "w")
    for row in array:
        file.write(",".join([str(x) for x in row])+"\n")
    file.close()


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


main()
