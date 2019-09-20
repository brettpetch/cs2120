def catstr(param1, param2):
    string = param1 + param2
    print(string)

def crosscat(p1, p2, p3, p4):
    return catstr(p1, p3), catstr(p2, p4)

crosscat("hello ", "world ", "its ", "me ")