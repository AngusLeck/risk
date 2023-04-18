import sys
from readWriteData import *
from likelihoodOfVictory import *
from expectedSurvivors import *


def main():
    # parse arguments
    attackers = int(sys.argv[1])
    defenders = int(sys.argv[2])
    shouldReadWrite = bool(sys.argv[3]) if len(sys.argv) > 3 else False

    # initialise variables
    maxDice = max(attackers, defenders, 200 if shouldReadWrite else 1)
    expectedSurvivorsArray = [[None]*maxDice for x in range(maxDice)]
    likelihoodOfVictoryArray = [[None]*maxDice for x in range(maxDice)]

    if (shouldReadWrite):
        readData("expectedSurvivors.txt", expectedSurvivorsArray)
        readData("likelihoodOfVictory.txt", likelihoodOfVictoryArray)

    # calculate expected result and chance
    chance = round(
        likelihoodOfVictory(
            attackers, defenders, likelihoodOfVictoryArray
        ) * 100,
        1
    )
    survivors = round(
        expectedSurvivors(
            attackers, defenders, expectedSurvivorsArray
        ),
        2
    )

    # inform user
    print(
        "likelihood of victory " + str(chance) + "% with "
        + str(survivors) + " survivors on average"
    )

    if (shouldReadWrite):
        writeData("expectedSurvivors.txt", expectedSurvivorsArray)
        writeData("likelihoodOfVictory.txt", likelihoodOfVictoryArray)

    return [chance, survivors]


main()
