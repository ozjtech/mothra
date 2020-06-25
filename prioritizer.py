import json
import random

interactionID = random.randint(1000, 10001)
possibleAnswers = ["y","Y","Yes.","yes","1more","anotha one","anotha1","I would like to add another task, yes."]

topPriority = []
lowPriority = []
leastPriority = []

myList = [topPriority,lowPriority,leastPriority]
def showList():
        print("Top Priority: ")
        print(topPriority)
        print("Low Priority: ")
        print(lowPriority)
        print("Least Priority: ")
        print(leastPriority)

class task:
        def __init__(self):
                self.value = input("What would you like to accomplish? ")
                self.priority = input("What is the priority of this task? least, low or high? ")
      
def prioritizer():
        newTask = task()
        if (newTask.priority == 'least'):
                leastPriority.append(newTask.value)
        if (newTask.priority == 'low'):
                lowPriority.append(newTask.value)
        if (newTask.priority == 'high'):
                topPriority.append(newTask.value)
        showList()

prioritizer()

def taskEngine():
        answer = input("Would you like to add another task? Y/N")
        if (answer in possibleAnswers): 
                prioritizer()
                taskEngine()
        else: print("Interaction ID: " + str(interactionID))

taskEngine()

with open("priorities.json", 'w') as myFile:
    # indent=2 is not needed but makes the file 
    # human-readable for more complicated data
    json.dump(myList, f, indent=2) 
    
with open("priorities.json", 'r') as myFile:
    myList = json.load(f)
