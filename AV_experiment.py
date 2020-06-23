from psychopy import data, visual, core, monitors
#import itertools
import v2_flash_stim as fs2
import random 
import numpy as np
import tdt


class Experiment():

	def __init__(self, numTrials=None, ISI=None, flash_dur=None, luminance=None, wave_freq=None,pulse_dur=None, wave_amp=None, auditory_on=None):

		self.numTrials=numTrials #number of trials
		self.ISI=ISI #interstimulus interval (time btw flashes, in seconds, for the flash stimulus)

		#flash stim specific
		self.flash_dur = flash_dur #time each flash lasts
		self.luminance = luminance

		#auditory stim. specific
		self.wave_freq=wave_freq #frequency (Hz)
		self.pulse_dur=pulse_dur #length of pulse (sound plays)
		self.wave_amp=wave_amp #volume of the sound
		self.auditory_on=auditory_on #boolean; determines whether there is an auditory component or not

	#takes in window parameters which can be changed as needed; provides flexibility
	def run_experiment(self, window_dim=[2560, 1600], screen_index=0, monitor_name="testMonitor"):

		#defining the window
		window=visual.Window(size=window_dim, 
			screen=screen_index, 
			monitor=monitor_name, 
			color=[0,0,0], 
			units='pix'
		)

		#instantiate a generic flash stimulus; will set the specifics of the parameters (pres_dur, luminance) later when it is randomly decided in the loop.
		flash = fs2.Flash_Stim(cur_screen=screen_index, cur_monitor=monitor_name, win_dim=window_dim, pres_dur=0, luminance=0)
		flash.autoDraw=True


		#create a dictionary of all the parameters; factorially combine to get all possible options
		factors={"ISI": self.ISI,
				"flash_dur": self.flash_dur,
				"luminance": self.luminance,
				"wave_freq": self.wave_freq, #waveFreq = freq of the tone
				"pulse_dur": self.pulse_dur, #pulseDur = length of time the tone is played
				"wave_amp": self.wave_amp, #waveAmp = sound levels
				"auditory_on": self.auditory_on
				}

		stimList = data.createFactorialTrialList(factors)
		 
		randNs = random.sample(range(0, len(stimList)-1), self.numTrials) # generate random numbers equal to the # of trials

		trials_subset = [None]*self.numTrials # since there are too many possiblilties we may only want a subset of them, so generate random numbers to choose which trials
		for i in range(0, self.numTrials):
			randNum = randNs[i]
			trials_subset[i] = stimList[randNum]




		#making experimentHandler and trials
		exp = data.ExperimentHandler(name='testExp', savePickle=True, saveWideText=True, dataFileName='experiment')

		trials = data.TrialHandler(trialList=trials_subset, nReps=3, method='sequential') # since already randomized we can go ahead and use "sequential" here...

		exp.addLoop(trials)


		#adding the data that we are collecting
		#trials.data.addDataType('Auditory Response')
		#trials.data.addDataType('Visual Response')

		#the experiment loop!
		for trial in trials:
			inter=trial['ISI']

		#	print(trial.items()) #access it like a dict
			if(trial['auditory_on']==True):
				print("===Auditory component on===\n *Play tone at %d dB*\n" %trial['wave_amp'])
				print("WF audio: " , trial['wave_freq'])
				core.wait(inter)

			else:
				trial['wave_freq']=None  # or "" looks cleaner in excel...but None probably better for loading into python
				trial['pulse_dur']=None
				trial['wave_amp']=None


			print("===No auditory===\n")
			dur = trial['flash_dur'] #pres. dur.
			lum = trial['luminance'] # luminance
			print("WF no audio: " , trial['wave_freq'])

			flash.pres_dur=dur
			flash.luminance=lum
			print("Luminance: ", lum)

			flash.flash(window)
			window.flip()
			core.wait(inter)

			exp.nextEntry()


def main():
	#Parameters:
	numTrials = 10
	ISI = [2, 3, 4, 5] #ISI in seconds

	#flash parameters
	flash_dur = [.001, .002] #flash durs in seconds (100 ms, 200 ms)
	luminance = [[1,1,1], [.86, .86, .86], [0,.1,1]] #white , grayish, purple just for testing

	#auditory parameters
	frequency = [1.1, 2.2, 3.3, 4.4] #waveFreq in TDT
	duration = [.001, .002, .003, .004] # in seconds; pulseDur in TDT
	sound_levels = [20, 40, 60, 80] # dB; waveAmp in TDT

	#Auditory on (T/F? if T then A+V, if F then Visual only)
	auditory_on = [True, False]				


	exper = Experiment(numTrials=numTrials, ISI=ISI, flash_dur=flash_dur, luminance=luminance, wave_freq=frequency,pulse_dur=duration, wave_amp=sound_levels, auditory_on=auditory_on)
	exper.run_experiment()

if __name__ == '__main__':
	main()






