from psychopy import data, visual, core, monitors
import itertools
import flash_stim as fs
import random # will use to randomize/shuffle
import numpy as np
import tdt

# TODO: hard-coded in values for now...refactor as class to take lists as params. 

#universal parameters
numTrials = 5
ISI = [2, 3, 4, 5] #ISI in seconds

#flash parameters
flash_dur = [.001, .002] #flash durs in seconds (100 ms, 200 ms)
luminance = [[1,1,1], [.86, .86, .86]] #white , grayish

#auditory parameters
frequency = [1.1, 2.2, 3.3, 4.4] #waveFreq in TDT
duration = [.001, .002, .003, .004] # in seconds; pulseDur in TDT
sound_levels = [20, 40, 60, 80] # dB; waveAmp in TDT

#Auditory on (T/F? if T then A+V, if F then Visual only)
auditory_on = [True, False]
#if this is false then we just include the first 3 vars (ISI, flash_dur, luminance..



#window variables:
win_dim=[2560, 1600]
screen_index=0
monitor_name="testMonitor"

#factorially combine the options into a dict. required by psychopy
factors={"ISI": ISI,
		"flash_dur": flash_dur,
		"luminance": luminance,
		"frequency": frequency, #waveFreq
		"duration": duration, #pulseDur
		"sound_levels": sound_levels, #waveAmp
		"auditory_on": auditory_on
		}

#make a randomized stimulus list
stimList = data.createFactorialTrialList(factors)
 
randNs = random.sample(range(0, len(stimList)-1), numTrials) # get random numbers equal to the # of trials

trials_subset = [None]*numTrials # to get a subset of values to use for the inputs from the overall massive stimlist
for i in range(0, numTrials):
	randNum = randNs[i]
	trials_subset[i] = stimList[randNum]

print(trials_subset)


trials = data.TrialHandler(trials_subset, nReps=1, method='sequential') # since already randomized we can go ahead and use "sequential" here...

#adding the data that we are collecting
trials.data.addDataType('Auditory Response')
trials.data.addDataType('Visual Response')
for i in range(0, numTrials):

	print(trial)
#	if(trial[auditory_on]==True):
#		print("Auditory component on\n")






#trials.saveAsPickle(fileName='testData')
#trials.saveAsWideText(fileName="trialData.xlsx")

