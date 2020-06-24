from psychopy import data, visual, core, monitors
import v2_flash_stim as fs2
import random 
import numpy as np
import tdt

#TODO: change flash_dur -> frames, do so by looping for n frames (for frame in range 0 to n, win.flip()...)


class Experiment():
	def __init__(self, numTrials=None, ISI=None, flash_dur=None, luminance=None, wave_freq=None,pulse_dur=None, wave_amp=None, stimulus=None):

		self.numTrials=numTrials #number of trials
		self.ISI=ISI #interstimulus interval (time btw flashes, in seconds, for the flash stimulus)

		#flash stim specific
		self.flash_dur = flash_dur #time each flash lasts
		self.luminance = luminance

		#auditory stim. specific
		self.wave_freq=wave_freq #frequency (Hz)
		self.pulse_dur=pulse_dur #length of pulse (sound plays)
		self.wave_amp=wave_amp #volume of the sound
		self.stimulus=stimulus #boolean; determines whether there is an auditory component or not

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
				"stimulus": self.stimulus
				}

		stimList = data.createFactorialTrialList(factors)
		 
		randNs = random.sample(range(0, len(stimList)-1), self.numTrials) # generate random numbers equal to the # of trials

		trials_subset = [None]*self.numTrials # since there are too many possiblilties we may only want a subset of them, so generate random numbers to choose which trials
		for i in range(0, self.numTrials):
			randNum = randNs[i]
			trials_subset[i] = stimList[randNum]




		#making experimentHandler and trials
		exp = data.ExperimentHandler(name='testExp', savePickle=True, saveWideText=True, dataFileName='experiment')

		trials = data.TrialHandler(trialList=trials_subset, nReps=1, method='sequential') # since already randomized we can go ahead and use "sequential" here...

		exp.addLoop(trials)

		#the experiment loop! 0: Auditory only; 1: Visual only; 2: A+V
		for trial in trials:
			inter=trial['ISI']

			if(trial['stimulus']==0): #auditory stim only
				print("===Auditory component only===\n *Play tone at %d dB*\n" %trial['wave_amp'])
				core.wait(inter)

			elif(trial['stimulus']==1): #visual stim only 
				trial['wave_freq']=None  # set all audio-related parameters to none 
				trial['pulse_dur']=None
				trial['wave_amp']=None

				print("===Visual component only===\n")
				dur = trial['flash_dur'] #pres. dur.
				lum = trial['luminance'] # luminance

				flash.pres_dur=dur
				flash.luminance=lum
				print("Luminance: ", lum)
				#present the stimulus
				flash.flash(window)
				window.flip()
				core.wait(inter)

			elif(trial['stimulus']==2): #A+V stim
				print("===Auditory and visual components on===\n *Play tone at %d dB*\n" %trial['wave_amp'])
				dur = trial['flash_dur'] #pres. dur.
				lum = trial['luminance'] # luminance

				flash.pres_dur=dur
				flash.luminance=lum
				print("Luminance: ", lum)
				#present the stimulus
				flash.flash(window)
				window.flip() #TODO: change to be timed by frame instead of seconds
				core.wait(inter)

			exp.nextEntry()


def main():
	#Parameters:
	numTrials = 10
	ISI = [2.0, 3.0, 4.0, 5.0] #ISI in seconds

	#flash parameters
	flash_dur = [.001, .002] #flash durs in seconds (100 ms, 200 ms)
	luminance = [[1,1,1], [.86, .86, .86], [0,.1,1]] #white , grayish, purple just for testing

	#auditory parameters
	frequency = [1.1, 2.2, 3.3, 4.4] #waveFreq in TDT
	duration = [.001, .002, .003, .004] # in seconds; pulseDur in TDT
	sound_levels = [20.0, 40.0, 60.0, 80.0] # dB; waveAmp in TDT

	#Auditory on (T/F? if T then A+V, if F then Visual only)
	stims={ 0: "auditory_only", 
			1: "visual_only",
			2: "A+V"
		}		


	exper = Experiment(numTrials=numTrials, ISI=ISI, flash_dur=flash_dur, luminance=luminance, wave_freq=frequency,pulse_dur=duration, wave_amp=sound_levels, stimulus=stims)
	exper.run_experiment()

if __name__ == '__main__':
	main()






