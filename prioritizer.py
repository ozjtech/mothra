topPriority = []
lowPriority = []
leastPriority = []

class task(object):
    value = input("What would you like to accomplish? ")


def findPriority(task): 
    priority = input("What is the priority of this task? least, low or high? ")
    if (priority == 'least'):
            leastPriority.append(task.value)
    if (priority == 'low'):
            lowPriority.append(task.value)
    if (priority == 'high'):
            topPriority.append(task.value)

findPriority(task)

print("High Priority:")
print(topPriority)
print("Low Priority: ")
print(lowPriority)
print("Least Priority: ")
print(leastPriority)