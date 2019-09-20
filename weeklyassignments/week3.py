## Name: Brett Petch
## Date: September 20, 2019

'''
Write a function convert_temperature that takes two arguments: a
float parameter temp, the temperature to convert; and a str parameter conversion that determines which conversion to
perform. Assume that conversion can take two possible values, 'celsius_to_fahrenheit' and 'fahrenheit_to_celsius',
and make 'celsius_to_fahrenheit' the default value. Have your function print out a sentence explaining the conversion
done, such as “0 °C converts to 32 °F”, and have the function return the converted value.

Your submission should include the function definition of followed by printing the result of three function calls:
one that uses the default conversion type, and two that explicitly specify the conversion type, one for each possible
conversion (Celsius to Fahrenheit and vice versa). You may (but are not required to) query the user for the input
temperatures.
'''


def convert_temperature(temp, conversion):

    if conversion == 'fahrenheit_to_celsius':
        fahrenheit_to_celsius = ((temp - 32) * (5 / 9))
        c = round(fahrenheit_to_celsius, 2)
    else:
        celsius_to_fahrenheit = (temp * 1.8000 + 32.00)
        c = round(celsius_to_fahrenheit, 2)
    print(str(temp) + " converts to " + str(c))


convert_temperature(32, 'fahrenheit_to_celsius')
convert_temperature(82, 'celsius_to_fahrenheit')
print("Hello, welcome to this simple program to convert temperature. ")
input1 = float(input("What is Temperature Value?: "))
input2 = str(input("What is conversion? Options are 'celsius_to_fahrenheit' and 'fahrenheit_to_celsius': "))
convert_temperature(input1, input2)
