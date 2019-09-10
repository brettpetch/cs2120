# Generate random number, assigned to an array of greetings.
import random
# Define Greetings
greetings = ["hello friend", "welcome", "greetings, meatbag.", "greetings human", "it won't be long now."]
# Generate a number based on the number of items in the array.
rand = random.randint(0, (len(greetings)-1))
# Print the greeting using the number generated using [c]
print(greetings[rand])