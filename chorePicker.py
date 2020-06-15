#Random is a module that helps us pick random numbers or items in a list.
import random
#Make a list of chores you need to do.
easyChores = ["Walk your dog",
"Clean your room",
"Do the dishes",
"Take out the trash",
"Check your mail"]

intermediateChores = ["Clean the kitchen",
"Do your laundry (Yes, all of it)",
"Clean your bathroom.",
"Organize the bookshelves"] 

hardChores = ["Deep clean the carpet.",
"Clean out the oven.",
"Organize the pantry and fridge.",
"Donate old stuff.",
"Schedule appointments."]

#Determine the users energy level
energyLevel = input("How much energy do you have, 1 and 3? ")

#Pick a random chore based on energy level
def choreHelper(energyLevel):
    if(energyLevel == '1'):
        print(random.choice(easyChores))
    if(energyLevel == '2'):
        print(random.choice(intermediateChores))
    if(energyLevel == '3'):
        print(random.choice(hardChores))

#CAll the function so it prints!
choreHelper(energyLevel)