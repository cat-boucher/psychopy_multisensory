from psychopy import data, visual, core, monitors
import itertools
import flash_stim as fs
import v2_flash_stim as fs2
import random # will use to randomize/shuffle
import numpy as np
import tdt

# TODO: hard-coded in values for now...refactor as class to take lists as params. 

#universal parameters
numTrials = 100
ISI = [2, 3, 4, 5] #ISI in seconds

#flash parameters
flash_dur = [.001, .002] #flash durs in seconds (100 ms, 200 ms)
luminance = [[1,1,1], [.86, .86, .86], [0,.1,1]] #white , grayish

#auditory parameters
frequency = [1.1, 2.2, 3.3, 4.4] #waveFreq in TDT
duration = [.001, .002, .003, .004] # in seconds; pulseDur in TDT
sound_levels = [20, 40, 60, 80] # dB; waveAmp in TDT

#Auditory on (T/F? if T then A+V, if F then Visual only)
auditory_on = [True, False]
#if this is false then we just include the first 3 vars (ISI, flash_dur, luminance..




#window variables:
window_dim=[2560, 1600]
screen_index=0
monitor_name="testMonitor"

window=visual.Window(size=window_dim, 
			screen=screen_index, 
			monitor=monitor_name, 
			color=[0,0,0], 
			units='pix'
		)

#create generic flash stimulus; will set the parameters later when it is actually decided in the loop.
flash = fs2.Flash_Stim(cur_screen=screen_index, cur_monitor=monitor_name, win_dim=window_dim, pres_dur=0, luminance=0)
flash.autoDraw=True

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
 
randNs = random.sample(range(0, len(stimList)-1), numTrials) # generate random numbers equal to the # of trials

trials_subset = [None]*numTrials # to get a subset of values to use for the inputs from the overall massive stimlist
for i in range(0, numTrials):
	randNum = randNs[i]
	trials_subset[i] = stimList[randNum]


#making experimentHandler and trials
exp = data.ExperimentHandler(name='testExp', savePickle=True, saveWideText=True, dataFileName='testExp')

trials = data.TrialHandler(trialList=trials_subset, nReps=1, method='sequential') # since already randomized we can go ahead and use "sequential" here...


#adding the data that we are collecting
trials.data.addDataType('Auditory Response')
trials.data.addDataType('Visual Response')

for trial in trials:
	print(trial.items()) #access it like a dict!
	if(trial['auditory_on']==True):
		print("===Auditory component on===\n *Play tone at %d dB*\n" %trial['sound_levels'])
	
	print("===No auditory===\n")
	dur = trial['flash_dur'] #pres. dur.
	lum = trial['luminance'] # luminance
	inter=trial['ISI']

	flash.pres_dur=dur
	flash.luminance=lum
	print("Luminance: ", lum)

	flash.flash(window)
	window.flip()
			





#trials.saveAsPickle(fileName='testData')
#trials.saveAsWideText(fileName="trialData.xlsx")

