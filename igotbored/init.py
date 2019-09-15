# Generate random number, assigned to an array of greetings.
import random

# names
names = ["karen", "meghan", "ken", "bob", "barbara", "george", "fred", "liam", "noah", "will", "james", "john", "mason",
         "oliver"]
# random names
randname = random.randint(0, (len(names) - 1))
# Define Greetings
greetings = ["hello " + (names[randname]), "welcome " + (names[randname]), "greetings meatbag, you must be " + (names[randname]), "greetings " + (names[randname]), "it won't be long now, " + (names[randname]),
             ("greetings " + (names[randname]) + " how's it going?")]
# Generate a number based on the number of items in the array.
rand = random.randint(0, (len(greetings)-1))
# Print the greeting using the number generated using [c]
print(greetings[rand])