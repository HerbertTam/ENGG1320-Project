from random import randint
import time

def constructRoad(width, length):
    road = []
    for i in range(width):
        section = []
        for j in range(length):
            section.append(0)
        road.append(section)
    return road

def printRoad(road, width):
    for i in range(width):
        print(road[i])

def dynmaicEnterRoad(road, width, ID, entryList,push_count):
    for i in range(width):
        if (randint(0,1) == 0):
            if (road[i][0] == 0):
                road[i][0] = ID
                entryList.append((push_count,ID))
                ID += 1
    return ID

def dynamicPushRoad(road, width, length, exitList,push_count):
    for i in range(width):
        for j in range(length):
            if (length-j-1 == 0):
                continue
            while(True):
                if (j == 0):
                    if (randint(0, 1)):
                        if (road[i][length-j-1] != 0):
                            exitList.append((push_count,road[i][length-j-1]))
                        road[i][length-j-1] = 0
                    else:
                        break
                if (road[i][length-j-1] != 0):
                    break
                if (randint(0, width)):
                    road[i][length-j-1] = road[i][length-j-2]
                    road[i][length-j-2] = 0
                    if (j - 1 >= 0):
                        j -= 1
                else:
                    break

def linearPushRoad(road, width, length, exitList,push_count):
    velocity = 2
    index_last = length - 1
    for i in range(width):
        for j in range(length):
            for k in range(velocity):
                if (road[i][index_last - j] != 0):
                    if (j == 0):
                        if (randint(0,10) == 0):
                            exitList.append((push_count, road[i][index_last - j]))
                            road[i][index_last - j] = 0
                        else:
                            break
                    elif road[i][index_last - j + 1] == 0:
                        road[i][index_last - j + 1] = road[i][index_last - j]
                        road[i][index_last - j] = 0
                        j -= 1

def pushRoad(road, width, length, entryList, exitList, push_count, ID, linear_count, dynamic_count, silence_count):
    while (True):
        modes = []
        if (linear_count > 0):
            modes.append('linear')
        if (dynamic_count > 0):
            modes.append('dynamic')
        if (silence_count > 0):
            modes.append('silence')
        if not modes:
            break
        mode = modes[randint(0,len(modes)-1)]
        if (mode == 'linear'):
            linearPushRoad(road, width, length, exitList, push_count)
            push_count += 1
            ID = dynmaicEnterRoad(road,width,ID,entryList,push_count)
            linear_count -= 1
        if (mode == 'dynamic'):
            dynamicPushRoad(road, width, length, exitList, push_count)
            push_count += 1
            ID = dynmaicEnterRoad(road,width,ID,entryList,push_count)
            dynamic_count -= 1
        if (mode == 'silence'):
            linearPushRoad(road, width, length, exitList,push_count)
            push_count += 1
            silence_count -= 1
    return ID, push_count

def updateTimer(exitList, entryList, timer):
    for exitRecord in exitList:
        for entryRecord in entryList:
            if exitRecord[1] == entryRecord[1]:
                timer.append((entryRecord[0]*60/29.97, round(exitRecord[0]-entryRecord[0])*60/29.97))

def main():
    width = 1
    length = 100
    road = constructRoad(width,length)

    ID = 1
    maxID = 10000
    push_count = 1
    timer = []
    entryList = []
    exitList = []
    while (True):
        linear_count = 2
        dynamic_count = 0
        silence_count = 8
        if (ID >= maxID/5):
            break
        ID, push_count = pushRoad(road, width, length, entryList, exitList, push_count, ID, linear_count, dynamic_count, silence_count)
    while (True):
        linear_count = 10
        dynamic_count = 0
        silence_count = 0
        if (ID >= 2*maxID/5):
            break
        ID, push_count = pushRoad(road, width, length, entryList, exitList, push_count, ID, linear_count, dynamic_count, silence_count)    
    while (True):
        linear_count = 2
        dynamic_count = 0
        silence_count = 8
        if (ID >= 3*maxID/5):
            break
        ID, push_count = pushRoad(road, width, length, entryList, exitList, push_count, ID, linear_count, dynamic_count, silence_count)    
    while (True):
        linear_count = 10
        dynamic_count = 0
        silence_count = 0
        if (ID >= 4*maxID/5):
            break
        ID, push_count = pushRoad(road, width, length, entryList, exitList, push_count, ID, linear_count, dynamic_count, silence_count)
    while (True):
        linear_count = 2
        dynamic_count = 0
        silence_count = 8
        if (ID >= maxID):
            break
        ID, push_count = pushRoad(road, width, length, entryList, exitList, push_count, ID, linear_count, dynamic_count, silence_count)
    updateTimer(exitList, entryList, timer)
    file = open("test_data.csv","w")
    file.write("entry time"+','+"time until re-identification\n")
    for entry_time, duration in timer:
        file.write(str(entry_time)+','+str(duration)+'\n')
    file.close
    print("written",len(timer),"records!")
main()