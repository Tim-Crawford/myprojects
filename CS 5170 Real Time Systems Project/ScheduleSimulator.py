import math
import time as t

Tasks = []
NextSchedPoint = 0

def AddTask():
    global Tasks
    
    task = input("Enter the name of task " + str(len(Tasks) + 1) + ": ")
    copyNum = 0
    for Task in Tasks:
        if task == Task[0]:
            task += "_("
            copyNum += 1
        if copyNum > 0:
            if task + str(copyNum) + ")" == Task[0]:
                copyNum += 1
    if copyNum > 0:
        task += str(copyNum) + ")"

    #Enter phase
    phase = -1
    while (phase < 0):
        try:
            phase = int(input("Enter the phase of task 1: "))
            if (phase < 0):
                print("Error phase cannot be negative.")
        except:
            print("Error enter a number.")

    #Enter period
    period = -1
    while (period <= 0):
        try:
            period = int(input("Enter the period of task 1: "))
            if (period <= 0):
                print("Error period cannot be negative or 0.")
        except:
            print("Error enter a number.")

    #Enter execution time
    execution = -1
    while (execution <= 0):
        try:
            execution = int(input("Enter the execution time of task 1: "))
            if (execution <= 0):
                print("Error execution time cannot be negative or 0.")
        except:
            print("Error enter a number.")

    #Enter deadline
    deadline = -1
    while (deadline <= phase):
        try:
            deadline = int(input("Enter the deadline of task 1: "))
            if (deadline <= phase):
                print("Error deadline cannot be less than or equal to the phase.")
        except:
            print("Error enter a number.")

    #Enter priority
    priority = -1
    while (priority != 0 and priority != 1):
        try:
            priority = int(input("Enter the priority of task 1: "))
            if priority != 0 and priority != 1:
                print("Error priority must be 0 or 1.")
        except:
            print("Error enter a number.")
    
    print("Added " + task + "(" + str(phase) + ", " + str(period) + ", " + str(execution) + ", " + str(deadline) + ", " + str(priority) + ")")
    Tasks.append([task, phase, period, execution, deadline, priority])
    return

def RemoveTask():
    global Tasks

    removed = input("Enter the name of the task you would like to remove: ")
    for task in Tasks:
        if removed == task[0]:
            Tasks.remove(task)
            print("Successfully removed " + removed + ".")
            return
    print(removed + " does not exist.")
    return

def LoadTasks():
    global Tasks
    fileName = input("Enter the name of the file you would like to load: ")
    try:
        file = open(fileName, "r")
        data = file.readlines()
        for i in data:
            task = i.split(',')
            copyNum = 0
            for Task in Tasks:
                if task[0] == Task[0]:
                    task[0] += "_("
                    copyNum += 1
                if copyNum > 0:
                    if task[0] + str(copyNum) + ")" == Task[0]:
                        copyNum += 1
            if copyNum > 0:
                task[0] += str(copyNum) + ")"
            Tasks.append([task[0], int(task[1]), int(task[2]), int(task[3]), int(task[4]), int(task[5][:-1])])
        file.close()
    except:
        print("Error trying to load from file.")
    return

def SaveTasks():
    global Tasks
    fileName = input("Enter the name of the file you would like to save to: ")
    try:
        file = open(fileName, "w+")
        for task in Tasks:
            file.write(task[0] + "," + str(task[1]) + "," + str(task[2]) + "," + str(task[3]) + "," + str(task[4]) + "," + str(task[5]) + "\n")
        file.close()
    except:
        print("Error trying to save to file.")
    return

def ListTasks():
    global Tasks
    if Tasks == []:
        print("No tasks currently exist.")
        return
    print("τi (φi, Ti, ei, Di, pi)\n-----------------------")
    for task in Tasks:
        print(task[0] + "(" + str(task[1]) + ", " + str(task[2]) + ", " + str(task[3]) + ", " + str(task[4]) + ", " + str(task[5]) + ")")
    return

def ClearTasks():
    global Tasks
    choice = "y"
    try:
        choice = input("Would you like to save first? (y/n): ")
    except:
        print("Error enter a number 1-8.")
    if choice == "y":
        SaveTasks()
    Tasks = []
    return

def Simulate(algorithm, numProcessors):
    taskList = []
    processors = []
    completedTasks = 0
    missedDeadlines = 0
    avgTardiness = 0.0
    preemptions = 0
    executionTime = 0
    hyperperiod = GetHyperperiod()
    for i in range(0,numProcessors):
        processors.append([])
    for time in range(0,hyperperiod):
        taskList = GetTaskList(taskList, time)
        t1_start = t.perf_counter()
        processors = algorithm(taskList, processors, time)
        t1_stop = t.perf_counter()
        executionTime += t1_stop - t1_start
        for p in processors:
            if p[time] != "":
                p[time][3] -= 1
                p[time] = p[time].copy()
                if p[time][3] == 0:
                    completedTasks += 1
                    if p[time][4] <= time:
                        missedDeadlines += 1
                        avgTardiness += time - p[time][4] + 1
                    try:
                        taskList.remove(p[time])
                    except:
                        time = time
                if time > 0:
                    if p[time-1] != "":
                        if p[time][0] != p[time-1][0]:
                            if p[time-1][3] != 0:
                                preemptions += 1
    print("\nCompleted Tasks:     " + str(completedTasks))
    print("Unfinished Tasks:    " + str(len(taskList)))
    print("Missed Dealines:     " + str(missedDeadlines))
    if missedDeadlines > 0:
        avgTardiness /= missedDeadlines
    print("Average Tardiness:   " + str(avgTardiness))
    print("Preemptions:         " + str(preemptions))
    print("Execution Time:      " + str(executionTime))
    '''for i in range(0,len(processors)):
        print("\nProcessor " + str(i))
        for time in range(0, len(processors[i])):
            print(str(time) + "    " + str(processors[i][time]))'''
    return

def GetHyperperiod():
    global Tasks
    period = 0
    if Tasks != []:
        period = Tasks[0][2]
        for i in range(1,len(Tasks)):
            period = lcm(period, Tasks[i][2])
    return period

def lcm(a,b): 
    return int((a*b) / math.gcd(a,b))

def GetTaskList(taskList, time):
    for task in Tasks:
        if (time - task[1]) % task[2] == 0:
            newTask = task.copy()
            newTask[0] += "_" + str(int((time - task[1]) / task[2]))
            newTask[1] = time
            newTask[4] += time
            newTask.append(newTask[3])
            taskList.append(newTask)
    return taskList

def EDF(taskList, processors, time):
    scheduled = []
    for p in processors:
        ED = 2147483647
        p.append("")
        for task in taskList:
            if task[4] < ED:
                if not task in scheduled:
                    ED = task[4]
                    p[-1] = task
        if p[-1] != "":
            scheduled.append(p[-1])
    return processors

def LST(taskList, processors, time):
    scheduled = []
    for p in processors:
        minSlack = 2147483647
        p.append("")
        for task in taskList:
            slack = task[4] - task[3] - time
            if slack < minSlack:
                if not task in scheduled:
                    minSlack = slack
                    p[-1] = task
        if p[-1] != "":
            scheduled.append(p[-1])
    return processors

def RM(taskList, processors, time):
    scheduled = []
    for p in processors:
        minPeriod = 2147483647
        p.append("")
        for task in taskList:
            if task[2] < minPeriod:
                if not task in scheduled:
                    minPeriod = task[2]
                    p[-1] = task
        if p[-1] != "":
            scheduled.append(p[-1])
    return processors

def SetupITSART(taskList, processors, time):
    global NextSchedPoint

    if NextSchedPoint == 0:
        running = []
        for i in range(0, len(processors)):
            running.append("")
            nextTask, NextSchedPoint = ITSART(taskList, running, time)
            processors[i].append(nextTask[1])
            running[i] = nextTask[1]
    elif time == NextSchedPoint:
        running = []
        for i in range(0, len(processors)):
            if processors[i][-1] != "":
                processors[i].append(processors[i][-1].copy())
                if processors[i][-1][3] <= 0:
                    processors[i][-1] = ""
            else:
                processors[i].append("")
            running.append(processors[i][-1])
        nextTask, NextSchedPoint = ITSART(taskList, running, time)
        if nextTask[1] != "":
            processors[nextTask[0]][-1] = nextTask[1]
    else:
        for i in range(0, len(processors)):
            if processors[i][-1] != "":
                processors[i].append(processors[i][-1].copy())
                if processors[i][-1][3] <= 0:
                    processors[i][-1] = ""
            else:
                processors[i].append("")
    return processors

def ITSART(taskList, running, time):
    selectedTask = [0, ""]
    if taskList != []:
        priorityList = []
        for task in taskList:
            if task[4]-time > 0:
                priorityList.append(math.log((task[4]-time)/task[3],2))
            else:
                priorityList.append(math.log((1/(time-task[4]+1))/task[3],2))
        nextCPU = LowestPriorityITSART(running, time)
        maxPriority = HighestPriority(taskList, priorityList)
        if nextCPU[1] == "" or nextCPU[0] > maxPriority[0]:
            running[nextCPU[2]] = maxPriority[1]
            taskList.remove(maxPriority[1])
            if nextCPU[1] != "":
                taskList.append(nextCPU[1])
            selectedTask = [nextCPU[2], maxPriority[1]]
    nextSchedPoint = min(TaskArrival(time), TaskTermination(running, time), CriticalMoment(taskList, time))
    return selectedTask, nextSchedPoint

def SetupSITSART(taskList, processors, time):
    global NextSchedPoint

    if NextSchedPoint == 0:
        running = []
        for i in range(0, len(processors)):
            running.append("")
            nextTask, NextSchedPoint = SITSART(taskList, running, time)
            processors[i].append(nextTask[1])
            running[i] = nextTask[1]
    elif time == NextSchedPoint:
        running = []
        for i in range(0, len(processors)):
            if processors[i][-1] != "":
                processors[i].append(processors[i][-1].copy())
                if processors[i][-1][3] <= 0:
                    processors[i][-1] = ""
            else:
                processors[i].append("")
            running.append(processors[i][-1])
        nextTask, NextSchedPoint = SITSART(taskList, running, time)
        if nextTask[1] != "":
            processors[nextTask[0]][-1] = nextTask[1]
    else:
        for i in range(0, len(processors)):
            if processors[i][-1] != "":
                processors[i].append(processors[i][-1].copy())
                if processors[i][-1][3] <= 0:
                    processors[i][-1] = ""
            else:
                processors[i].append("")
    return processors

def SITSART(taskList, running, time):
    selectedTask = [0, ""]
    if taskList != []:
        priorityList = []
        for task in taskList:
            priorityList.append((task[4] - time - task[3])/task[3])
        nextCPU = LowestPrioritySITSART(running, time)
        maxPriority = HighestPriority(taskList, priorityList)
        if nextCPU[1] == "" or nextCPU[0] > maxPriority[0]:
            running[nextCPU[2]] = maxPriority[1]
            taskList.remove(maxPriority[1])
            if nextCPU[1] != "":
                taskList.append(nextCPU[1])
            selectedTask = [nextCPU[2], maxPriority[1]]
    nextSchedPoint = min(TaskArrival(time), TaskTermination(running, time), CriticalMoment(taskList, time))
    return selectedTask, nextSchedPoint

def LowestPriorityITSART(taskList, time):
    minPriority = [-2147483647, "", 0]
    for i in range(0,len(taskList)):
        if taskList[i] == "":
            return [2147483647, "", i]
        if taskList[i][4]-time > 0:
            priority = math.log((taskList[i][4]-time)/taskList[i][3],2)
        else:
            priority = math.log((1/(time-taskList[i][4]+1))/taskList[i][3],2)
        if minPriority[0] < priority:
            minPriority = [priority, taskList[i].copy(), i]
    return minPriority

def LowestPrioritySITSART(taskList, time):
    minPriority = [-2147483647, "", 0]
    for i in range(0,len(taskList)):
        if taskList[i] == "":
            return [2147483647, "", i]
        priority = (taskList[i][4]-time-taskList[i][3])/taskList[i][3]
        if minPriority[0] < priority:
            minPriority = [priority, taskList[i], i]
    return minPriority

def HighestPriority(taskList, priorityList):
    maxPriority = [2147483647, ""]
    for i in range(0,len(taskList)):
        if priorityList[i] < maxPriority[0]:
            maxPriority = [priorityList[i], taskList[i]]
    return maxPriority

def TaskArrival(time):
    global Tasks
    minArrivalTime = 2147483647
    for task in Tasks:
        if time >= task[1]:
            arrivalTime = math.ceil((time - task[1] + 1)/task[2]) * task[2] + task[1]
            if arrivalTime < minArrivalTime:
                minArrivalTime = arrivalTime
    return minArrivalTime

def TaskTermination(taskList, time):
    minTermination = 2147483647
    for task in taskList:
        if task != "":
            termination = time + task[3]
            if termination < minTermination:
                minTermination = termination
    return minTermination

def CriticalMoment(taskList, time):
    minCM = 2147483647
    for task in taskList:
        #D - c(t)
        CM = task[4] - task[3]
        if CM < minCM:
            minCM = CM
    if minCM <= time:
        return time+1
    return minCM

def IEDF(taskList, processors, time):
    #sort tasklist into high and low priority lists
    highTaskList = []
    lowTaskList = []
    for task in taskList:
        if task[5] == 1:
            highTaskList.append(task)
        else:
            lowTaskList.append(task)
    if len(highTaskList) > 0:
        highTaskList = SortPriority(highTaskList, time)
    if len(lowTaskList) > 0:
        lowTaskList = SortPriority(lowTaskList, time)
    for p in processors:
        if len(highTaskList) > 0:
            if highTaskList[0][3] + time == highTaskList[0][4]:
                p.append(highTaskList[0])
                highTaskList.remove(highTaskList[0])
                continue
            #wait time + time execution must begin > deadline
            if (time - highTaskList[0][1]) + (highTaskList[0][3] + time) > highTaskList[0][4]:
                p.append(highTaskList[0])
                highTaskList.remove(highTaskList[0])
                continue
        if len(lowTaskList) > 0:
            if lowTaskList[0][3] + time == lowTaskList[0][4]:
                p.append(lowTaskList[0])
                lowTaskList.remove(lowTaskList[0])
                continue
            if (time - lowTaskList[0][1]) + (lowTaskList[0][3] + time) > lowTaskList[0][4]:
                p.append(lowTaskList[0])
                lowTaskList.remove(lowTaskList[0])
                continue
        if len(highTaskList) > 0:
            p.append(highTaskList[0])
            highTaskList.remove(highTaskList[0])
        elif len(lowTaskList) > 0:
            p.append(lowTaskList[0])
            lowTaskList.remove(lowTaskList[0])
        else:
            p.append("")
    return processors

def SortPriority(taskList, time):
    sort = [taskList[0]]
    priorities = [sort[0][4] - time - sort[0][3]]
    for i in range(1, len(taskList)):
        newP = taskList[i][4] - time - taskList[i][3]
        for j in range(0, len(sort)):
            if newP < priorities[j]:
                sort.insert(j, taskList[i])
                priorities.insert(j, newP)
                break
            if j == len(sort)-1:
                sort.append(taskList[i])
                priorities.append(newP)
    return sort

def URM(n):
    return n*(2**(1/n)-1)

#kv = 0.1716
#kc = 0.656
#ke = 0.1724
#Vi = task[5]
#Ci = task[6]
#Ei = task[4] - time
#Pi = kv * Vi + kc * (sum(j=1 to N) Ci)/Ci + ke * (sum(j=1 to N) Ei)/Ei
#Ui = task[3]/(task[4]-time)
#P'i = Pi/Ui
def EDFHeapsort(taskList, processors, time):
    C = 0
    E = 0
    for task in taskList:
        C += task[6]
        E += time-task[2]+1
    priorities = []
    for i in range(0, len(taskList)):
        P = -0.1716*taskList[i][5] + 0.656*(C/taskList[i][6]) + 0.1724*(E/(time-task[2]+1))
        priorities.append([P/(taskList[i][6]/taskList[i][2]), i])
    HeapSort(priorities)
    for p in processors:
        if len(priorities) > 0:
            p.append(taskList[priorities[0][1]])
            priorities.remove(priorities[0])
        else:
            p.append("")
    return processors

def HeapSort(arr): 
    n = len(arr)
  
    # Build a maxheap. 
    for i in range(n//2 - 1, -1, -1): 
        heapify(arr, n, i) 
  
    # One by one extract elements 
    for i in range(n-1, 0, -1): 
        arr[i], arr[0] = arr[0], arr[i] # swap 
        heapify(arr, i, 0)

def heapify(arr, n, i): 
    largest = i # Initialize largest as root 
    l = 2 * i + 1     # left = 2*i + 1 
    r = 2 * i + 2     # right = 2*i + 2 
  
    # See if left child of root exists and is 
    # greater than root 
    if l < n and arr[i][0] < arr[l][0]: 
        largest = l 
  
    # See if right child of root exists and is 
    # greater than root 
    if r < n and arr[largest][0] < arr[r][0]: 
        largest = r 
  
    # Change root, if needed 
    if largest != i: 
        arr[i],arr[largest] = arr[largest],arr[i] # swap 
  
        # Heapify the root. 
        heapify(arr, n, largest)

def ListETF(taskList, processors, time):
    scheduled = []
    for p in processors:
        ETF = 2147483647
        p.append("")
        for task in taskList:
            if task[1] < ETF:
                if not task in scheduled:
                    ETF = task[1]
                    p[-1] = task
        if p[-1] != "":
            scheduled.append(p[-1])
    return processors
    
def AlgorithmMenu():
    global NextSchedPoint
    global Tasks

    while True:
        print("\n--------------")
        print("| Algorithms |")
        print("--------------")
        print("1. EDF")
        print("2. LST")
        print("3. RM")
        print("4. ITSA-RT")
        print("5. SITSA-RT")
        print("6. IEDF")
        print("7. EDF-Heapsort")
        print("8. List-ETF")
        print("9. Back")
        choice = 0
        while choice <= 0 or choice > 9:
            try:
                choice = int(input("Select a number 1-9: "))
                if choice <= 0 or choice > 8:
                    print("Error enter a number 1-9.")
            except:
                print("Error enter a number 1-9.")
        if choice == 9:
            return
        numProcessors = 0
        while numProcessors <= 0:
            try:
                numProcessors = int(input("How many processors to simulate: "))
                if numProcessors <= 0:
                    print("Error enter a number that is greater than 0.")
            except:
                print("Error enter a number.")
        algorithm = EDF
        if choice == 2:
            algorithm = LST
        elif choice == 3:
            algorithm = RM
        elif choice == 4:
            NextSchedPoint = 0
            algorithm = SetupITSART
        elif choice == 5:
            NextSchedPoint = 0
            algorithm = SetupSITSART
        elif choice == 6:
            algorithm = IEDF
        elif choice == 7:
            u = 0.0
            for task in Tasks:
                u += task[3]/task[2]
            if u > 1:
                algorithm = EDFHeapsort
        elif choice == 8:
            algorithm = ListETF
        Simulate(algorithm, numProcessors)

#Menu Loop
run = True
while(run):
    print("\n----------------------")
    print("| Schedule Simulator |")
    print("----------------------")
    print("1. Add Task")
    print("2. Remove Task")
    print("3. Load Tasks")
    print("4. Save Tasks")
    print("5. List Tasks")
    print("6. Clear Tasks")
    print("7. Simulate Schedule")
    print("8. Exit")
    choice = 0
    while choice <= 0 or choice > 8:
        try:
            choice = int(input("Select a number 1-8: "))
            if choice <= 0 or choice > 8:
                print("Error enter a number 1-8.")
        except:
            print("Error enter a number 1-8.")
    if choice == 1:
        AddTask()
    elif choice == 2:
        RemoveTask()
    elif choice == 3:
        LoadTasks()
    elif choice == 4:
        SaveTasks()
    elif choice == 5:
        ListTasks()
    elif choice == 6:
        ClearTasks()
    elif choice == 7:
        AlgorithmMenu()
    elif choice == 8:
        run = False
