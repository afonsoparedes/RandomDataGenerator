import string
import random
import rstr
from datetime import datetime
from datetime import timedelta


fname = input("Insert file name\n")
dili = input("Insert delimiter\n")
colNum = int(input("Insert number of columns\n"))
times = int(input("Insert number of lines of data\n"))

colTypes = []
colRestrains = []
listNum = 0
listRest = []

def generateInt(low,up):
    return random.randrange(low,up)

def generateString(min,max):
    x = generateInt(min,max)
    ret = ''.join(random.choice(string.ascii_lowercase) for x in range(x))
    return ret


def generateRegex(regex):
    return rstr.xeger(regex)


def generateDate(low,up):
    end = datetime.strptime(up, '%Y-%m-%d %H:%M')
    start = datetime.strptime(low, '%Y-%m-%d %H:%M')

    
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return (start + timedelta(seconds=random_second)).strftime("%Y-%m-%d %H:%M")


def generateList(listType,rest,listNum):
    ret = []
    listLen = generateInt(listRest[listNum][0],listRest[listNum][1])
    if listType == "int":
        for i in range(listLen):
            ret.append(generateInt(rest[0],rest[1]))
    elif listType == "string":
        for i in range(listLen):
            ret.append(generateString(rest[0],rest[1]))
    elif listType == "date":
        for i in range(listLen):
            ret.append(generateDate(rest[0],rest[1]))
    elif listType == "regex":
        for i in range(listLen):
            ret.append(generateRegex(rest))
    else:
        print("WRONG TYPE")
        exit(1)
    return ret
    
def typeVerif(colType,isList):
    if colType == "sequence" and not isList:
        colRestrains.append(int(input("Insert initial sequence value\n")))
    elif colType == "constant" and not isList:
        colRestrains.append(input("Insert constant value\n"))
    elif colType == "int":
        rest = []
        if isList:
            rest.append(int(input("Select lower bound for int from list\n")))
            rest.append(int(input("Select upper bound for int from list\n")))
        else:
            rest.append(int(input("Select lower bound for int\n")))
            rest.append(int(input("Select upper bound for int\n")))
        colRestrains.append(rest)
    elif colType == "string":
        rest = []
        if isList:
            rest.append(int(input("Select min number of characters for string from list\n")))
            rest.append(int(input("Select max number of characters for string from list\n")))
        else:
            rest.append(int(input("Select min number of characters for string\n")))
            rest.append(int(input("Select max number of characters for string\n")))
        colRestrains.append(rest)
    elif colType == "regex":
        if(isList):
            colRestrains.append(input("Select regex pattern to generate Strings in List\n"))
        else:
            colRestrains.append(input("Select regex pattern to generate Strings\n"))
    elif colType == "date":
        rest = []
        if isList:
            rest.append(input("Select lower bound for date (Y-M-D H:M) from list\n"))
            rest.append(input("Select upper bound for date (Y-M-D H:M) from list\n"))
        else:
            rest.append(input("Select lower bound for date (Y-M-D H:M)\n"))
            rest.append(input("Select upper bound for date (Y-M-D H:M)\n"))
        colRestrains.append(rest)
    elif colType[:4] == "list" and not isList:
        rest = []
        rest.append(int(input("Select min number of list elements\n")))
        rest.append(int(input("Select max number of list elements\n")))
        listRest.append(rest)
        typeVerif(colType[5:],True)
    else:
        print("ERROR: WRONG TYPE")
        exit(1)

#Types & restrains
for i in range(colNum):
    colTypes.append(input("Select column " + str(i+1) +" type. (regex,sequence,constant,int,string,date,list:typeOfList(list:regex,list:int,list:string,list:date))\n"))
    typeVerif(colTypes[i],False)


#Generation
fp = open(fname,"w")

lines = []
for n in range(times):
    line = ""
    for i in range(colNum):
        if colTypes[i] == "sequence":
            line += str(colRestrains[i])
            colRestrains[i] += 1
        elif colTypes[i] == "regex":
            line += generateRegex(colRestrains[i])
        elif colTypes[i] == "constant":
            line += colRestrains[i]
        elif colTypes[i] == "int":
            line += str(generateInt(colRestrains[i][0],colRestrains[i][1]))
        elif colTypes[i] == "string":
            line += generateString(colRestrains[i][0],colRestrains[i][1])
        elif colTypes[i] == "date":
            line += generateDate(colRestrains[i][0],colRestrains[i][1])
        elif colTypes[i][:4] == "list":
            line += str(generateList(colTypes[i][5:],colRestrains[i],listNum))
            listNum += 1
        else:
            print("WRONG TYPE" + colNum[i])
            exit(1)
        if i < (colNum - 1):
            line += dili
        else:
            line += "\n"
    listNum = 0
    fp.write(line)

print("FILE CREATED SUCCESSFULLY\n")