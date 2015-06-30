import simpy
import numpy as np
import matplotlib.pyplot as plt

'''Doctor office simpy
Model people arriving for routine visits, with early and late
'''


APPOINTMENT_LENGTH = 14  # allocated time per patient
APPOINTMENT_STDEV = 2  # stdeviation of patient appoitnment
ARRIVAL_SIG = 5
ARRIVAL_MEAN = 15
SIM_TIME = 10*60 #10 hours, in minutes
WAITING_ROOM_CAP = 30


waitTimesPerPatient = []

# class office():
# 	def __init__(self, params, env):
# 		self.env = env



def patient(env, scheduledTime, doc, num):
	arriveTime = env.now
	with doc.request() as req:
		yield req
		print("Patient sees doctor.  Scheduled:",scheduledTime, "Present time:",env.now)
		wait = env.now
		waitTime = env.now- arriveTime
		waitTimesPerPatient.append((num, waitTime))
		print("Wait Time:", waitTime)
		yield env.process(examinePatient(env, num))
		leaveTime = env.now-wait
		print("Leave Time:", leaveTime)
	#request doctor


def examinePatient(env, num):
	print("Examining patient", num)
	delay = np.random.normal(0,APPOINTMENT_STDEV, 1)
	duration = APPOINTMENT_LENGTH + max(0, delay)
	yield env.timeout(duration)
	print("Done with patient",num)


def arrivalProcess( env, doc):
	nextTime = ARRIVAL_MEAN
	currentTime = ARRIVAL_MEAN
	scheduledTime = ARRIVAL_MEAN
	count = 1
	while True:
		#delay or arrive earlier than needed
		nextArrival = np.random.normal(0, ARRIVAL_SIG,1)
		currentTime += nextArrival
		currentTime = max(currentTime, 0)
		nextTime -= nextArrival
		yield env.timeout(currentTime)
		print("Patient",count,"arrived")
		env.process(patient(env, scheduledTime, doc, count))
		count+=1
		currentTime = nextTime
		nextTime = ARRIVAL_MEAN
		scheduledTime += nextTime




env =  simpy.Environment()
doctor = simpy.Resource(env, capacity = 1)
env.process(arrivalProcess(env, doctor))
env.run(until = SIM_TIME)

x,y = zip(*waitTimesPerPatient)
plt.plot(x,y)
plt.show()





