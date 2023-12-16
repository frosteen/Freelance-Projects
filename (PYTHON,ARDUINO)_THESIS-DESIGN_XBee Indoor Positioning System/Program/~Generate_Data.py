import random

with open("Data.txt", "a") as file:
    file.write("\n")
    file.write("0 13 A2 0 41 48 64 0E,68 65 6C 6C," + str(random.randrange(-60, -28)))
    file.write("\n")
    file.write("0 13 A2 0 41 26 3B B7,68 65 6C 6C," + str(random.randrange(-60, -28)))
    file.write("\n")
    file.write("0 13 A2 0 41 26 3B B8,68 65 6C 6C," + str(random.randrange(-60, -28)))
