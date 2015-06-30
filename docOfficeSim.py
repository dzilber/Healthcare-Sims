import simpy
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

'''Doctor office simpy
Model people arriving for routine visits, with early and late
'''


APPOINTMENT_LENGTH = 14  # allocated time per patient
APPOINTMENT_STDEV = 2  # stdeviation of patient appoitnment
ARRIVAL_SIG = 5
ARRIVAL_MEAN = -5
SIM_TIME = 10*60 #10 hours, in minutes
WAITING_ROOM_CAP = 30


waitTimesPerPatient = []

# class office():
# 	def __init__(self, params, env):
# 		self.env = env



def patient(param_b, env, scheduledTime, doc, num):
	arriveTime = env.now
	with doc.request() as req:
		yield req
		print("Patient sees doctor.  Scheduled:",scheduledTime, "Present time:",env.now)
		wait = env.now
		waitTime = env.now- arriveTime
		waitTimesPerPatient.append((num, waitTime))
		print("Wait Time:", waitTime)
		yield env.process(examinePatient(param_b, env, num))
		leaveTime = env.now-wait
		print("Leave Time:", leaveTime)
	#request doctor


def examinePatient(param_b, env, num):
	avg, stdev = param_b
	print("Examining patient", num)
	delay = np.random.normal(0,stdev, 1)
	duration = avg + max(0, delay)
	yield env.timeout(duration)
	print("Done with patient",num)


def arrivalProcess(param_a, param_b, env, doc):
	mu, stdev = param_a
	nextTime = mu
	currentTime = mu
	scheduledTime = mu
	count = 1
	while True:
		#delay or arrive earlier than needed
		nextArrival = np.random.normal(0, stdev,1)
		currentTime += nextArrival
		currentTime = max(currentTime, 0)
		nextTime -= nextArrival
		yield env.timeout(currentTime)
		print("Patient",count,"arrived")
		env.process(patient(param_b, env, scheduledTime, doc, count))
		count+=1
		currentTime = nextTime
		nextTime = mu
		scheduledTime += nextTime



n=1/4
paramSets = [(15,j) for j in np.arange(1,6,n)]
combos = [(i,j) for i in paramSets for j in paramSets]


data = []
for v in combos:
	waitTimesPerPatient = []
	v_a, v_b = v
	env =  simpy.Environment()
	doctor = simpy.Resource(env, capacity = 1)
	env.process(arrivalProcess(v_a, v_b, env, doctor))
	env.run(until = 600)

	x,y = zip(*waitTimesPerPatient)
	data.append((v_a[1], v_b[1], np.average(y)))



inv = 1/n

x=np.arange(1,6,n)
y=np.arange(1,6,n)
X,Y = np.meshgrid(x,y)

Z = np.zeros((len(x),len(x)))
for row in data:
	x,y,z = row
	Z[inv*(y-1), inv*(x-1)] = z

# norm = cm.colors.Normalize(vmax=abs(Z).max(), vmin=-abs(Z).max())
cmap = plt.cm.GnBu
plt.contourf(X, Y, Z, cmap = cmap)
plt.show()





