import sys
from src.parseArguments import *
from src.readWriteData import *
from src.likelihoodOfVictory import *
from src.expectedSurvivors import *


def main():
    args = parseArguments()
    attackers = args.attackers
    defenders = args.defenders

    # initialise variables
    maxDice = max(attackers, defenders, 200 if args.write else 1)
    expectedSurvivorsArray = [[None]*maxDice for x in range(maxDice)]
    likelihoodOfVictoryArray = [[None]*maxDice for x in range(maxDice)]
    sys.setrecursionlimit(args.recursionLimit)

    if (args.read):
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

    if (args.write):
        writeData("expectedSurvivors.txt", expectedSurvivorsArray)
        writeData("likelihoodOfVictory.txt", likelihoodOfVictoryArray)

    return [chance, survivors]
