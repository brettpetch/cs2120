# Name: Brett Petch
# Date: September 11, 2019
# Week 2 - Basic Python Strings, Variables, Integers and Floats.

# Create expressions to: add two variables
a = 10
b = 30
c = 5
result1 = (a + b)

print(str(a) + str(" + ") + str(b) + " = " + (str(result1)))
print(" ")

# multiply two variables then add a third
result2 = (a * b + c)
print(str(a) + (str(" * ") + str(b) + str(" + ") + str(c) + str(" = ") + str(result2)))
print()

# divide the expression from 1 by the expression of 2
print(str(result1) + str(" / ") + str(result2) + str(" = ") + str(result1 / result2))
print()

# convert a temperature in fahrenheit to celcius
fahrenheit = 72
celcius = ((fahrenheit - 32) * (5 / 9))
print(str(fahrenheit) + str(" degrees fahrenheit is ") + str(celcius) + str(" degrees celcius."))

# convert a temperature in celcius to kelvin
kelvin = celcius + 273.15
print("which is also " + str(kelvin) + " degrees kelvin.")
