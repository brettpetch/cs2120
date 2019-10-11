# Brett Petch
# October 2nd, 2019
# Week 4 Activity Lecture


def vowel_counter(sentence):
    """
    :function vowel_counter: counts amount of vowels in string.
    :param sentence:
    :var vowels: counter for amount of vowels in string
    :var char: amount of characters in sentence.
    :var lists: vowels - lists vowels to search for
    :var num: keeps track of each counter, stored in list for easy calling
    :return: how many values of vowel were present in your string.
    """
    vowels = ['A', 'E', "I", "O", "U"]
    num = [0, 0, 0, 0, 0]

    for letter in range(len(sentence)):
        for v in range(len(vowels)):
            if sentence[letter] == vowels[v]:
                num[v] += 1

    for letter in range(len(vowels)):
        print("There are", num[letter], vowels[letter], "s in the sentence '", sentence, "'")


def input_sterilization():
    """

    :param: none
    :return: sterilized input
    :exception if there is an issue with values, it will repeat the loop.
    """
    while True:
        try:
            input1 = str(input("Please enter a sentence.: "))
        except ValueError:
            print("Invalid Input!")
            continue
        else:
            return input1
            break


# Delete the part that has a static string to reveal an easter egg!
words = "Hello darkness; my old friend" or input_sterilization()
vowel_counter(words.upper())

words = "i like pancakes :)" or input_sterilization()
vowel_counter(words.upper())

words = "let's have fun with this! i love life!" or input_sterilization()
vowel_counter(words.upper())
