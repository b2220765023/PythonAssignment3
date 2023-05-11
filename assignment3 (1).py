# Yusuf Emir Cömert - 2220765023 - Assignment 3 - Vodafone Park Stadium
from itertools import product
import sys

input = sys.argv[1]
score = "-"
stadiums = {}
categoryDetail = {}
seats = []


def read():                                     # basic read function 
    global input_file
    input_file = open(input , 'r')


def write(text):
    toprint = "".join(text)
    print(toprint)
    output_file.writelines(text)
    output_file.writelines(('\n'))


def create(command):
    createdCategory = command[15:].rstrip('\n').split(" ")
    cartesian = createdCategory[1].split("x")
    rows = []
    columns = []

    for i in range(65, int(cartesian[0]) + 65):
        rows.append(chr(i))
    for i in range(0, int(cartesian[1])):
        columns.append(i)
    seats = list(product(rows, columns))
    seatorder = []

    for i in range(len(seats)):
        order = seats[i][0] + str(seats[i][1])
        seatorder.append(order)

    temp = createdCategory[0]
    createdCategory[0] = {"name": temp, "empty": []}
    tempdict = createdCategory[0]

    if createdCategory[0]["name"] not in categoryDetail:  # we could see whether the new category should be added with only names list
        categoryDetail[(createdCategory[0]["name"])] = cartesian
        tempdict["empty"] = "empty", seatorder          # in this part, our dictionary becomes the last form
        stadiums[createdCategory[0]["name"]] = createdCategory[0]
        write(("The category '", temp, "' having ", str(int(categoryDetail[temp][0]) * (int(categoryDetail[temp][1])))," seats has been created."))
    else:
        write(("Warning: Cannot create the category for the second time. The stadium has already " + createdCategory[0]["name"] + "."))


def sellTicket(command):
    seatPurchased = []
    soldTicket = command[11:].rstrip('\n').split(" ")            # .rstrip method removes any trailing characters(characters at the end a string)
    customer = soldTicket[0]
    ticketType = soldTicket[1]
    categoryName = soldTicket[2]
    multisold = []                                               # I used this list for record multiple selling, for example when we want to buy between A4-8

    for i in range(3, len(soldTicket)):
        if any(c in score for c in soldTicket[i]):
            seatRange = soldTicket[i][1:].split(score)
            letter = [soldTicket[i][0]]
            if ord(letter[0]) > 65 + int(categoryDetail[categoryName][0]) - 1:
                write(("Error: The category ", categoryName, " has less row than the specified index ", soldTicket[i], "!"))            #errors and stuffs
            else:
                if int(seatRange[1]) > int(categoryDetail[categoryName][1]) - 1:
                    write(("Error: The category ", categoryName, " has less column than the specified index ", soldTicket[i],"!"))      #errors and stuffs
                else:
                    seatList = []
                    for a in range(int(seatRange[0]), int(seatRange[1]) + 1):
                        if letter[0] + str(a) in stadiums[categoryName]["empty"][1]:
                            multisold.append(letter[0] + str(a))
                            seatList = []
                            canbuy = True
                        else:
                            write(("Warning: The seats ", soldTicket[i], " cannot be sold to ", customer, " due some of them have already been sold!"))     #warnings and stuffs
                            canbuy = False
                            break

                        seatList.append(a)
                    if canbuy: write(("Success: ", customer, " has bought ", soldTicket[i], " at ", categoryName))      #successes of buy
                    wholesale = list(product(letter, seatList))
                    for a in range(len(wholesale)):
                        multisold.append(wholesale[a][0] + str(wholesale[a][1]))

        else:
            if ord(soldTicket[i][0]) > 65 + int(categoryDetail[categoryName][0]) - 1:
                write(("Error: The category ", categoryName, " has less row than the specified index ", soldTicket[i], "!"))        #index error    
            else:
                if int(soldTicket[i][1:]) > int(categoryDetail[categoryName][1]) - 1:
                    write(("Error: The category ", categoryName, " has less column than the specified index ", soldTicket[i],"!"))  #index error
                else:
                    if soldTicket[i] in stadiums[categoryName]["empty"][1]:
                        seatPurchased.append(soldTicket[i])
                        write(("Success: ", customer, " has bought ", soldTicket[i], " at ", categoryName))
                    else:
                        write(("Warning: The seat ", soldTicket[i], " cannot be sold to ", customer, " since it was already sold!"))    #already sold error

    totalsale = seatPurchased + multisold
    duplicate = []
    for i in range(len(totalsale)):
        try:
            stadiums[categoryName]["empty"][1].remove(totalsale[i])
        except:
            duplicate.append(totalsale[i])
    stadiums[categoryName][customer] = ticketType, totalsale
    for i in range(len(duplicate)):
        stadiums[categoryName][customer][1].remove(duplicate[i])


def cancelTicket(command):
    tocancel = command[13:].rstrip('\n').split(" ")
    categoryName = tocancel[0]
    for i in range(1, len(tocancel)):
        seattocancel = tocancel[i]
        if ord(seattocancel[0]) > 65 + int(categoryDetail[categoryName][0]) - 1:
            write(("Error: The category ", categoryName, " has less row than the specified index ", seattocancel, "!"))         #index error
            seattocancel = "ı"
        else:
            if int(seattocancel[1:]) > int(categoryDetail[categoryName][1]) - 1:
                write(("Error: The category ", categoryName, " has less column than the specified index ", seattocancel, "!"))  #index error
                seattocancel = "ı"
            else:
                pass
        for key in stadiums[categoryName]:
            if seattocancel in stadiums[categoryName][key][1]:
                if key == "empty":
                    write(("Error: The seat ", seattocancel, " at '",categoryName,"' has already been free! Nothing to cancel"))            #already free error
                else:
                    write(("Success: The seat ", seattocancel, " at '",categoryName,"' have been canceled and now ready to sell again"))    #successes of calcelling 
                    stadiums[categoryName][key][1].remove(seattocancel)
                    stadiums[categoryName]["empty"][1].append(seattocancel)


def balance(command):
    categoryName = command[8:].rstrip('\n')
    revenue = {"student" : 0,"full": 0,"season": 0,}
    for key in stadiums[categoryName]:
        if key == "name":
            pass
        elif key == "empty":
            pass
        else:
            revenue[stadiums[categoryName][key][0]] = len(stadiums[categoryName][key][1])
    profit = revenue["student"] * 10 + revenue["full"] * 20 + revenue["season"] * 250           #student= 10$ , full = 20$ , season = 250$
    write(("category report of '",categoryName,"'\n-------------------------------\n"
                                               "Sum of studens = ",str(revenue["student"]),
                                               ", Sum of full pay = ",str(revenue["full"]),             
                                               ", Sum of season ticket = ", str(revenue["season"]),
                                               ", and Revenues = ", str(profit), " Dollars"))


def showcategory(command):
    categoryName = command[13:].rstrip('\n')
    categoryList = []
    categoryDict = {}
    categoryNumber = []
    categoryLetter = []
    data = []
    for i in range(0, int(categoryDetail[categoryName][1])):
        categoryNumber.append(i)


    for i in range(0, int(categoryDetail[categoryName][0])):
        seatId = chr(i + 65)
        categoryLetter.append(seatId)
        for a in range(0, len(categoryNumber)):
            seatId = categoryLetter[i] + str(categoryNumber[a])
            for key in stadiums[categoryName]:
                if seatId in stadiums[categoryName][key][1]:
                    if key == "empty":                  #  if the seat number is in empty list, this puts "X" to the table
                        categoryDict[seatId] = "X"
                    else:
                        if stadiums[categoryName][key][0] == "student":         #  if the seat number is in student list, this puts "S" to the table
                            categoryDict[seatId] = "S"
                        elif stadiums[categoryName][key][0] == "full":          #  if the seat number is in full list, this puts "F" to the table
                            categoryDict[seatId] = "F"
                        elif stadiums[categoryName][key][0] == "season":        #  if the seat number is in season list, this puts "T" to the table
                            categoryDict[seatId] = "T"


    write(("Printing category layout of", categoryName))
    row_format = "{:3}" * (len(categoryNumber) + 1)
    for row in range(0, len(categoryNumber)):
        data.append([])
        for i in range(int(categoryDetail[categoryName][1])):
            data[row].append(categoryDict[categoryLetter[-row - 1] + str(categoryNumber[i])])
        write((categoryLetter[-row - 1], row_format.format("", *data[row])))
    write((row_format.format("", *categoryNumber)))


read()
count = 0
output_file = open('output.txt', 'w')                   # this command is for writing output file

while True:                                             # This is the main loop of this assignment and easiest loop of the assignment
    count += 1
    line = input_file.readlines()
    global a
    for a in range(len(line)):
        if line[a].startswith("CREATECATEGORY"):
            create(line[a])
        elif line[a].startswith("SELLTICKET"):
            sellTicket(line[a])
        elif line[a].startswith("CANCELTICKET"):
            cancelTicket(line[a])
        elif line[a].startswith("BALANCE"):
            balance(line[a])
        else:
            showcategory(line[a])
    if not line:
        break
