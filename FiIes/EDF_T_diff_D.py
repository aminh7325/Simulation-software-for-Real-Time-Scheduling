import copy
from math import ceil, gcd
import matplotlib.pyplot as plt
import numpy as np

Tasks = dict()
RealTime_Task = dict()
# For gantt chart
y_axis  = []
from_x = []
to_x = []
y_axis_Miss = []
from_x_Miss = []
to_x_Miss = []
Complete_Period = []

def Read_Data():
    
	"""
	Reading the details of the tasks to be scheduled from the user as
	Number of tasks N:
	Period of task P:
	Worst case excecution time C:
	"""
	global N
	global HP
	global Tasks

	N = int(input("\n \t\tEnter number of Tasks:"))
	# Storing data in a dictionary

	for i in range(N):
		Tasks[i] = {}
		print("\n Enter Period of task T",i,":")
		P = input()
		Tasks[i]["Period"] = int(P)
		print("Enter the WCET of task C",i,":")
		C = input()
		Tasks[i]["WCET"] = int(C)
		print("Enter the DeadLine of task D",i,":")
		D = input()
		Tasks[i]["DeadLine"] = int(D)
		Complete_Period.append(0)

def UtilizationCalc():
    
    """
    For Finding system Utilization and Check Bounds
    """
    U = 0
    for i in range(N):
        U = U + Tasks[i]["WCET"]/Tasks[i]["DeadLine"]
    
    return U

def PriorityCalc(RealTime_task , PPriority):
    
	"""
	Estimates the priority of tasks at each real time period during scheduling
	"""
	HP = 10000
	TempDeadLine = HP
	P = -1    #Returns -1 for idle tasks
	for i in RealTime_task.keys():
		if (RealTime_task[i]["WCET"] != 0):
			if (TempDeadLine > RealTime_task[i]["DeadLine"]):
				TempDeadLine = RealTime_task[i]["DeadLine"] #Checks the priority of each task based on DeadLine
				P = i
			elif (TempDeadLine == RealTime_task[i]["DeadLine"] and PPriority != -1 and RealTime_task[PPriority]["WCET"] != 0 ):
				#Give priority to task that is undergoing
				P = PPriority
                
	return P

    
def Simulation(hp):

	"""
	The real time schedulng based on Rate Monotonic scheduling is simulated here.
	"""
	# Real time scheduling are carried out in RealTime_task
	global RealTime_task
	RealTime_task = copy.deepcopy(Tasks)
	PPriority = -1
	# main loop for simulator
    
	for t in range(hp):

		# Determine the priority of the given tasks
		Priority = PriorityCalc(RealTime_task , PPriority)
		PPriority = Priority
        
		if (Priority != -1):
			# Update WCET after each clock cycle
			RealTime_task[Priority]["WCET"] -= 1
			# For plotting the results
   
			#print("T is:" , t , "  Deadline is:" , (Complete_Period[Priority] + 1 )*Tasks[Priority]["DeadLine"])
			if t < RealTime_task[Priority]["DeadLine"]:
				y_axis.append("TASK%d"%(Priority+1)+" (" + "C =%d"%Tasks[Priority]["WCET"] + ")")
				from_x.append(t)
				to_x.append(t+1)
			else:
				y_axis_Miss.append("TASK%d"%(Priority+1)+" (" + "C =%d"%Tasks[Priority]["WCET"] + ")")
				from_x_Miss.append(t)
				to_x_Miss.append(t+1)

		# Update Period after each clock cycle
		for i in RealTime_task.keys():
			RealTime_task[i]["Period"] -= 1
			if (RealTime_task[i]["Period"] == 0 ):
				if (RealTime_task[i]["WCET"] == 0):
					Complete_Period[i] += 1
					RealTime_task[i]["DeadLine"] = Tasks[i]["Period"] * (Complete_Period[i]) + Tasks[i]["DeadLine"]
					RealTime_task[i]["WCET"] = copy.deepcopy(Tasks[i]["WCET"])
					RealTime_task[i]["Period"] = copy.deepcopy(Tasks[i]["Period"])
				else:
					RealTime_task[i]["Period"] = copy.deepcopy(Tasks[i]["Period"])
        		    




def DrawGraph():
	"""
	The scheduled results are displayed in the form of a
	gantt chart for the user to get better understanding
	"""
	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	# the data is plotted from_x to to_x along y_axis
	ax = plt.hlines(y_axis, from_x, to_x, linewidth=20, color = 'green')
	if from_x_Miss != []:
		ax = plt.hlines(y_axis_Miss, from_x_Miss, to_x_Miss, linewidth=20, color = 'red')
	plt.title('Earliest-Deadline First scheduling')
	plt.grid(True)
	plt.xlabel("Real-Time clock")
	plt.ylabel("HIGH<------------------Priority--------------------->LOW")
	plt.xticks(np.arange(min(from_x), max(to_x)+1, 1.0))
	plt.show()
 
Read_Data()
hp = 40
Simulation(hp)
Us = UtilizationCalc()
if Us <= 1:
    print("We can Use EDF for scheduling because Us <= 1 \n Us:" , Us)
else:
	print("We Can't use EDF for scheduling because Us > 1 \n Us:" , Us)
DrawGraph()