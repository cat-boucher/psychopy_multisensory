from psychopy import data, visual, core, monitors, event
import v2_flash_stim as fs2
import random 
import numpy as np
import PhotodiodeMarker as pdm
import time
import tdt
from synapse_experiment import get_params, set_params


#TODO: change flash_dur -> frames, do so by looping for n frames (for frame in range 0 to n, win.flip()...)


class Experiment():
	def __init__(self, numTrials=None, ISI=None, flash_dur=None, luminance=None, wave_freq=None,pulse_dur=None, wave_amp=None, stimulus=None, delay=None):

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

		self.delay=delay #Between presentation of auditory and visual stimulus within the trial. In ms

		#hard-coded timings within the code
		self.pre_stim = 8 # initial wait time before the stimulus presentation starts
		self.jitter = 0.250 #250 ms jitter 



	#takes in window parameters which can be changed as needed; provides flexibility
	def run_experiment(self, window_dim=[800, 600], screen_index=0, monitor_name="testMonitor"):

		#temporary, just for testing bc i get errors since I dont have synapse. set to true if actually connecting to synapse
		CONNECT = False
		if(CONNECT):
			# Connect to Synapse
			syn = tdt.SynapseAPI()

		#defining the window
		window=visual.Window(size=window_dim, 
			screen=screen_index, 
			monitor=monitor_name, 
			color=[0,0,0], 
			units='pix'
		)

		#instantiate a generic flash stimulus; will set the specifics of the parameters (pres_dur, luminance) later when it is randomly decided in the loop.
		flash = fs2.Flash_Stim(cur_screen=screen_index, cur_monitor=monitor_name, win_dim=window_dim, pres_dur=0, luminance=0)
	#	flash.autoDraw=True


		#create a dictionary of all the parameters; factorially combine to get all possible options
		factors={"ISI": self.ISI,
				"flash_dur": self.flash_dur,
				"luminance": self.luminance,
				"wave_freq": self.wave_freq, #waveFreq = freq of the tone
				"pulse_dur": self.pulse_dur, #pulseDur = length of time the tone is played
				"wave_amp": self.wave_amp, #waveAmp = sound levels
				"stimulus": self.stimulus,
				"delay": self.delay # delay between presenting A and V
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

		marker = pdm.PhotodiodeMarker()

		#load values into the buffer before the trial starts...
		params_list = get_params(trials)
		
		if(CONNECT):
			set_params(params_list) 

	#	print(params_list)

	#	event.waitKeys(keyList='space') #could put this in to have the actual experiment (1st pdm flash, etc.) start on keypress

		#the experiment loop! 0: Auditory only; 1: Visual only; 2: A+V
		for trial in trials:
			inter=trial['ISI']

			#initial marker flash for each trial
			for n in range(0, self.pre_stim*60):
				if n<10: #draw the marker for 10 frames
					marker.draw_marker(window)
					
			window.flip()

			# jitter = wait time before first stimulus: 
			core.wait(self.jitter) 
			time.sleep(.375) #maximum delay if presenting auditory before visual plus maybe 30-50% ~250ms + 125 = 375ms

			#these are already loaded into the buffer ? 
		#	if(CONNECT):
		#			#set the auditory value decided by Psychopy in Synapse: WaveAmp, WaveFreq, Delay (?)
		#			syn.setParameterValue('aStim2', 'WaveAmp', trial['wave_amp'])
		#			syn.setParameterValue('aStim2', 'WaveFreq', trial['wave_freq'])
		#			syn.setParameterValue('aStim2', 'PulseDur', trial['pulse_dur'])
		#			syn.setParameterValue('aStim2', 'StimID', trial['stimulus']+1) 


			if(trial['stimulus']==0): #auditory stim only

				print("===Auditory component only===\n *Play tone at %d dB*\n" %trial['wave_amp'])
				trial['delay']=None

			elif(trial['stimulus']==1): #visual stim only 
				trial['wave_freq']=None  # set all audio-related parameters to none 
				trial['pulse_dur']=None
				trial['wave_amp']=None
				trial['delay']=None
				if(CONNECT):
					#set the auditory value decided by Psychopy in Synapse: WaveAmp, WaveFreq, Delay (?)
					syn.setParameterValue('aStim2', 'WaveAmp', 0) # set all values to 0  bc no auditory
					syn.setParameterValue('aStim2', 'WaveFreq', 0)
					syn.setParameterValue('aStim2', 'PulseDur', 0)


				print("===Visual component only===\n")
				dur = trial['flash_dur'] #pres. dur.
				lum = trial['luminance'] # luminance

				flash.pres_dur=dur
				flash.luminance=lum

				print("Luminance: ", lum)
				#present the stimulus
				flash.flash(window)
				marker.draw_marker(window)
				window.flip()


			elif(trial['stimulus']==2): #A+V stim
				#option 1: Audio first: delay -
				if(trial['delay'] < 0): #delay = time between A and V within the trial
					print("===Auditory and visual components on: A first ===\n *Play tone at %d dB*\n" %trial['wave_amp'])


					# wait while the audio is going + the delay btw stimuli
					total_wait = abs(trial['delay'])+trial['pulse_dur'] 
					print("Waiting for tone to play: " ,trial['pulse_dur'] )
					print("Waiting (stimulus delay): " ,trial['delay'])

					core.wait(total_wait)


					dur = trial['flash_dur'] #pres. dur.
					lum = trial['luminance'] # luminance

					flash.pres_dur=dur
					flash.luminance=lum

					print(trial['delay'])

					print("Luminance: \n", lum)
					#present the stimulus
					flash.flash(window)
					marker.draw_marker(window)
					window.flip() #TODO: change to be timed by frame instead of seconds
			

				#option 2: Visual first: delay +
				if(trial['delay'] > 0):

					print("===Auditory and visual components on: V first ===\n *Play tone at %d dB*\n" %trial['wave_amp'])
					dur = trial['flash_dur'] #pres. dur.
					lum = trial['luminance'] # luminance

					flash.pres_dur=dur
					flash.luminance=lum


					print("Luminance: \n", lum)
					#present the stimulus
					flash.flash(window)
					marker.draw_marker(window)
					window.flip() #TODO: change to be timed by frame instead of seconds

					total_wait = trial['delay']+trial['pulse_dur'] # after visual presented, need to wait the delay btw stimuli + the duration of the audio pulse
					print("Waiting (stimulus delay): " ,trial['delay'])
					print("Waiting for tone to play: " ,trial['pulse_dur'])
					core.wait(total_wait)


				#option 3: Simultaneous: delay 0 
				# TODO: add a second flash BEFORE the stimulus? 
				if(trial['delay'] == 0):
					print("===Auditory and visual components on: Simultaneous ===\n *Play tone at %d dB*\n" %trial['wave_amp'])
					dur = trial['flash_dur'] #pres. dur.
					lum = trial['luminance'] # luminance

					flash.pres_dur=dur
					flash.luminance=lum

					print("Luminance: \n", lum)
					#present the stimulus
					flash.flash(window)
					marker.draw_marker(window)
					window.flip() #TODO: change to be timed by frame instead of seconds
			
			print("Waiting ISI Time: ", inter, '\n')
			core.wait(inter-self.jitter) #inter stimulus interval = time between successive presentations
			window.flip()

			exp.nextEntry()


def main():
	#Parameters:
	numTrials = 10
	ISI = [2.0, 3.0, 4.0, 5.0] #ISI in seconds: time between trials
	delay = [-50.0, -25.0, -10.0, 0.0, 10.0, 25.0, 50.0] # *change to ms* ; time between presentation of A + V within a trial. (-) A first, (+) V first 

	#flash parameters
	flash_dur = [.001, .002, .1] #flash durs in seconds (100 ms, 200 ms)
	luminance = [[1,1,1], [.86, .86, .86], [0,.1,1]] #white , grayish, purple just for testing

	#auditory parameters: input them as the actual desired unit (Hz, ms, dB) -> will get converted if needed within the code.
	frequency = [1.1, 2.2, 3.3, 4.4] #Hz;waveFreq in TDT
	duration = [.001, .002, .003, .004] # in ms; pulseDur in TDT
	sound_levels = [20.0, 40.0, 60.0, 80.0] # dB; waveAmp in TDT

	stims={ 0: "auditory_only", 
			1: "visual_only",
			2: "A+V"
		}		


	exper = Experiment(numTrials=numTrials, ISI=ISI, flash_dur=flash_dur, luminance=luminance, wave_freq=frequency,pulse_dur=duration, wave_amp=sound_levels, stimulus=stims, delay=delay)
	exper.run_experiment()

if __name__ == '__main__':
	main()






