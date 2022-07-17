"""
Version 0.5.1
2022-07-05

-New Stuff-
-Added support for positional parameters to set army sizes

A small python script for automating dice-rolls when playing Risk. Since, you know, that can get
tedious after a while late-game. Prompts for the size of each army, asks for a stop-loss and prompts 
for how many attacks to do. 

Rolls all the dice and changes the army size accordingly then asks if you want to continue.

Basic functionality is there (for now), but I plan to expand on this over time as a for-fun passion project
to keep brushing-up on my Python. Completely built from the ground-up by me (for now, contributions are
welcome)

Planned updates: 
- Log all dice-rolls and start running stats on them 
- GUI? (once I start playing around with GUI frameworks maybe) 
"""

import random, sys 

################################
###   Function Definitions   ###
################################

#Functions that run every attack to calculate the number of dice to roll for each army
def diceCountAtk(armySize):
    if armySize >= 4:
        return 3
    elif armySize == 3:
        return 2
    else:
        return 1

def diceCountDef(armySize):
    if armySize == 1:
        return 1
    else:
        return 2


#Runs after the inital number prompt to read the value and make sure it's a number
def numberPrompt():
    blah = input()
    while not isinstance(blah, int):
        if blah == "":
            blah = 1
        try:
            blah = int(blah)
        except:
            blah = input("Try again: ")
    return blah

def attackNumber():
    print("How many attacks (leave blank for 1):", end="")
    numAttacks = numberPrompt()
    return numAttacks

#The actual attack function
def attack():

    global atkArmy
    global defArmy
    global allAtkRolls
    global allDefRolls

    #Creating the empty lists to store the dice roll values
    atkRolls = []
    defRolls = []

    #Sets a variable for the number of dice to role
    atkDice = diceCountAtk(atkArmy)
    defDice = diceCountDef(defArmy)

    #"Rolls the dice" for each side and appends the values to the empty lists
    #Also appends the value to the stat lists
    for i in range(atkDice):
        atkRolls.append(random.randint(1,6))
        allAtkRolls.append(atkRolls[-1])
        allRolls.append(atkRolls[-1])    
    for i in range(defDice):
        defRolls.append(random.randint(1,6))
        allDefRolls.append(defRolls[-1])
        allRolls.append(defRolls[-1])
    

    #Sorting the results of the rolls 
    atkRolls.sort(reverse=True)
    defRolls.sort(reverse=True)

    #Printing the dice rolls
    print("The attackers rolled:", atkRolls)
    print("The defenders rolled:", defRolls)

    #Loops over the dice rolls of the defending army and decrements the army size for the losing side
    diceCount = 0
    for i in defRolls:
        #Breaks early if only 1 attacking die is rolled
        if diceCount + 1 > len(atkRolls):
            break
        if defRolls[diceCount] >= atkRolls[diceCount]:
            atkArmy -= 1
        else:
            defArmy -= 1
        diceCount += 1
    
    print("New number of attackers:", atkArmy)
    print("New number of defenders:", defArmy)

    return 0



############################
###   Start of program   ###
############################

#Initializing some stat variables

#Number of attacks
atkCount = 0

#List of all of the dice rolls, overall and one for each army 
#To be used later as part of tracking dice-rolls
allRolls = []
allAtkRolls = []
allDefRolls = []


# Checks for positional parameters, set them as the army sizes if they're numbers
# First parameter = attacking army
# Second parameter = defending army

if sys.argv[1]:
    try:
        atkArmy = int(sys.argv[1])
    except ValueError:
        print("Enter the number of attackers: ", end="")
        atkArmy = numberPrompt()
        while atkArmy < 2:
            print("Can't attack with less than 2 troops. Enter the number of attackers:", end="")
            atkArmy = numberPrompt()

if sys.argv[2]:
    try:
        defArmy= int(sys.argv[2])
    except ValueError:
        print("Enter the number of defenders: ", end="")
        defArmy = numberPrompt()
        while atkArmy < 2:
            print("Can't attack with less than 2 troops. Enter the number of defenders:", end="")
            atkArmy = numberPrompt()


print("Enter army size to stop attacking (leave blank to fight to the last man):", end="")
stopLoss = numberPrompt()


while atkArmy > stopLoss and defArmy > 0:
    numAttacks = attackNumber()
    for i in range(numAttacks):
        atkCount += 1   
        print("Attack number:", atkCount)
        attack()
        if atkArmy == stopLoss or defArmy == 0:
            break

    if atkArmy == stopLoss or defArmy == 0:
        break

    more = input("Continue attacking? (Y/n): ")
    if more == "n" or more == "N":
        break

#Printing the results of the dice rolls
print("All dice rolls:", allRolls)
print("Total number of dice rolled:", len(allRolls))
allRollsStats = {number: allRolls.count(number) for number in allRolls}
print(allRollsStats)

print("All attack rolls:", allAtkRolls)
print("Total number of attack dice rolled:", len(allAtkRolls))
allAtkRollsStats = {number: allAtkRolls.count(number) for number in allAtkRolls}
print(allAtkRollsStats)

print("All defence rolls:", allDefRolls)
print("Total number of defence dice rolled:", len(allDefRolls))
allDefRollsStats = {number: allDefRolls.count(number) for number in allDefRolls}
print(allDefRollsStats)