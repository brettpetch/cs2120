# Generate random number, assigned to an array of greetings.
import random

# names
names = ["karen", "meghan", "ken", "bob", "barbara", "george", "fred", "liam", "noah", "will", "james", "john", "mason",
         "oliver"]
# random names
randname = random.randint(0, (len(names) - 1))
# Define Greetings
greetings = ["hello ", "welcome ", "greetings meatbag, you must be ", "greetings ", "it won't be long now, ",
             ("greetings " + (names[randname]) + " how's it going?")]
# Generate a number based on the number of items in the array.
rand = random.randint(0, (len(greetings)-1))
# Print the greeting using the number generated using [c]
if greetings.index(names[randname]):
    print(greetings[rand])
else:
    print((greetings[rand]) + (names[randname]))
