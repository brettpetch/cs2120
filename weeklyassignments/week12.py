# Student Name:
# Student Number:
# Grade: 100 %


def fact(n):
    """
    This function will calculate the factorial of n using recursion.
    :param n: what factorial?
    :return: factorial
    """
    if n == 1:
        return n
    else:
        return n*fact(n - 1)


print(fact(5))
