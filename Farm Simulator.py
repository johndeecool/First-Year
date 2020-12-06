import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)


#CREATING AND FILLING EXTENDED TEMPLATE
def farmOpener(file):

    values = []

    f = open(file, "r")

    for i in f:
        values.append(i.split())

    x = int(values[0][0])
    farmtemplate = np.full((x + 2, x + 2), "_")

    firefruit = values[1]
    firefruit2 = []
    for i in range(0, len(firefruit)):
        firefruit2.append(firefruit[i].split(","))

    waterfruit = values[2]
    waterfruit2 = []
    for i in range(0, len(waterfruit)):
        waterfruit2.append(waterfruit[i].split(","))

    grassfruit = values[3]
    grassfruit2 = []
    for i in range(0, len(grassfruit)):
        grassfruit2.append(grassfruit[i].split(","))

    joltfruit = values[4]
    joltfruit2 = []
    for i in range(0, len(joltfruit)):
        joltfruit2.append(joltfruit[i].split(","))


    #FIRE
    for i in range(0, len(firefruit2)):
        farmtemplate[int(firefruit2[i][0]) + 1, int(firefruit2[i][1]) + 1] = "F"
    #WATER
    for i in range(0, len(waterfruit2)):
        farmtemplate[int(waterfruit2[i][0]) + 1, int(waterfruit2[i][1]) + 1] = "W"
    #GRASS
    for i in range(0, len(grassfruit2)):
        farmtemplate[int(grassfruit2[i][0]) + 1, int(grassfruit2[i][1]) + 1] = "G"
    #JOLT
    for i in range(0, len(joltfruit2)):
        farmtemplate[int(joltfruit2[i][0]) + 1, int(joltfruit2[i][1]) + 1] = "J"

    return farmtemplate


#SCANNING FARM ADJACENCY
def bodyScanner(farmsegment):

    body = []

    for i in range(0, len(farmsegment) - 2):

        scanned = [[0], [0], [0], [0], [0]]

        h = farmsegment[i : i + 3, 0 : 3]

        row1 = str(h[0])
        row2left = str(h[1][0])
        row2right = str(h[1][2])
        row3 = str(h[2])

        scanner = row1 + " " + row2left + " " + row2right + " " + row3

        scanned[0] = scanner.count("F")
        scanned[1] = scanner.count("W")
        scanned[2] = scanner.count("G")
        scanned[3] = scanner.count("J")

        if str(h[1][1]) == "_":
            scanned[4] = "empty"

        elif str(h[1][1]) == "F" or "W" or "G" or "J":
            scanned[4] = str(h[1][1])

        body.append(scanned)

    return body


#TABULATING ADJACENCY DATA
def readScanner(data):

    growthdata = []

    for i in range(0, len(data) - 2):
        growthdata.append(bodyScanner(data[0: , i : i + 3]))

    return growthdata


#DETERMINING SPRING GROWTH
def springTime(tabular, row):

    counter = []

    for i in tabular:
        if i[row][4] != "empty":
            counter.append(i[row][4])

        elif i[row][4] == "empty":

            #MEGA
            if i[row][0] > 0 and i[row][1] > 0 and i[row][2] > 0 and i[row][3] > 0:
                counter.append("M")
            #JOLT
            elif i[row][3] > 0:
                counter.append("J")
            #NON-DOMINANCE
            elif i[row][0] > 0 and i[row][1] > 0 and i[row][2] > 0 and i[row][3] < 1:
                counter.append("_")
            #FIRE
            elif i[row][0] >= 1 and i[row][1] < 1 and i[row][3] < 1:
                counter.append("F")
            #GRASS
            elif i[row][2] >= 1 and i[row][0] < 1 and i[row][3] < 1:
                counter.append("G")
            #WATER
            elif i[row][1] >= 1 and i[row][2] < 1 and i[row][3] < 1:
                counter.append("W")
            #NONE
            else:
                counter.append("_")

    return counter


#RESIZING POST - GROWTH FARM
def resize(springfunction, scanner):

    farm = []

    for i in range(0, len(scanner)):

        if i == 0:
            farm.append(['_'] * len(scanner))

        farm.append(springfunction(scanner, i))

        if i == len(scanner) - 1:
            farm.append(['_'] * len(scanner))

    for i in range(len(farm)):

        farm[i].insert(0, '_')
        farm[i].insert(len(farm), '_')

    return np.array(farm)


#SIMULATING YEARS
def simulation(firstfarm, nextfarm, year):

    a = firstfarm
    b = nextfarm

    firecount = np.count_nonzero(b == "F")
    watercount = np.count_nonzero(b == "W")
    grasscount = np.count_nonzero(b == "G")
    joltcount = np.count_nonzero(b == "J")
    megacount = np.count_nonzero(b == "M")

    if (np.array_equal(firstfarm, nextfarm)) == True:

        print("Total yield from final year!")
        print("Firefruit: " + str(firecount))
        print("Waterfruit: " + str(watercount))
        print("Grassfruit: " + str(grasscount))
        print("Joltfruit: " + str(joltcount))
        print("Megafruit: " + str(megacount))

        return a

    else:

        print("Total yield after " + str(year) + " year(s)!")
        print("Firefruit: " + str(firecount))
        print("Waterfruit: " + str(watercount))
        print("Grassfruit: " + str(grasscount))
        print("Joltfruit: " + str(joltcount))
        print("Megafruit: " + str(megacount))
        print(" ")

        return simulation(b, resize(springTime,readScanner(b)), year + 1)

palf = farmOpener("pokefruit_palletfarm.txt")
virf = farmOpener("pokefruit_viridianfarm.txt")
saff = farmOpener("pokefruit_saffronfarm.txt")
celf = farmOpener("pokefruit_celadonfarm.txt")
pewf = farmOpener("pokefruit_pewterfarm.txt")


#SELECTING FARM OUTPUT
print("1 = Pallet")
print("2 = Viridian")
print("3 = Saffron")
print("4 = Celadon")
print("5 = Pewter")
print("")
user = input("Please select a farm: ")
print("")

if user == "1":
    simulation(palf, resize(springTime,readScanner(palf)), 1)
if user == "2":
    simulation(virf, resize(springTime,readScanner(virf)), 1)
if user == "3":
    simulation(saff, resize(springTime,readScanner(saff)), 1)
if user == "4":
    simulation(celf, resize(springTime,readScanner(celf)), 1)
if user == "5":
    simulation(pewf, resize(springTime,readScanner(pewf)), 1)



