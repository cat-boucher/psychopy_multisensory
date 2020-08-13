from psychopy import data, visual, core, monitors, event
import v2_flash_stim as fs2
import random 
import numpy as np
import PhotodiodeMarker as pdm
import time
import tdt
import synapse_experiment as synex
#from psychopy import logging
#logging.console.setLevel(logging.INFO)



class Experiment():
	def __init__(self, numTrials=None, ISI=None, flash_dur=None, luminance=None, wave_freq=None,pulse_dur=None, wave_amp=None, stimulus=None, delay=None, SYN_CONNECTED=False):
		"""	
		Experiment: class to run a multisensory integration experiment with custom timing and stimulus presentation.
		-----------

		Attributes:
		-----------
		numTrials: int
			number of trials in the experiment
		ISI: float
			interstimulus interval; time between flashes for the flash stimulus. (unit: seconds)

		flash_dur: float
			time each flash lasts (unit: ms)
		luminance: 
			color of the flash. input as list of 3 numbers from [-1, 1] where -1 is black, 1 is white (ex. [-1, 0, 1])
		
		wave_freq: float
			frequency (Hz)
		pulse_dur: float
			length of pulse (ms)
		wave_amp: float
			volume of the sound (dB)
		stimulus: 
			dictionary: 0 (A only), 1 (V only) , or 2 (A+V)

		delay: 
			interstimulus delay between presentation of auditory and visual stimulus WITHIN the trial. Input in ms;  (-) A first, (+) V first 

		JITTER: float
			wait time before first stimulus (intrinsic delay). Hard-coded. (input in ms)
		SYSTEM_DELAY: float
			communication delay time between the 2 computers. Hard-coded value, measure + change in the lab. (input in ms)

		Functions:
		----------

		"""

		self.numTrials=numTrials 
		self.ISI=ISI 

		#flash stim specific
		self.flash_dur = flash_dur 
		self.luminance = luminance 

		#auditory stim. specific
		self.wave_freq=wave_freq 
		self.pulse_dur=pulse_dur 
		self.wave_amp=wave_amp 
		self.stimulus=stimulus 

		self.delay=delay 

		#hard-coded timings within the code
		self.JITTER = 250.0  #250 ms jitter 
		self.SYSTEM_DELAY = 200.0 # (temporary) 200 ms delay btw stimulus computer and recording computer. TODO: change this once the real timing is recorded in lab
		self.SYN_CONNECTED = SYN_CONNECTED

	
	def rand_trials_sample(self):
		"""
		generates a randomized list of trial/stimulus parameters, of length numTrials
		"""
		factors={"ISI_s": self.ISI,
				"flash_dur_ms": self.flash_dur,
				"luminance": self.luminance,
				"wave_freq_Hz": self.wave_freq, #waveFreq = freq of the tone
				"pulse_dur_ms": self.pulse_dur, #pulseDur = length of time the tone is played
				"wave_amp_dB": self.wave_amp, #waveAmp = sound levels
				"stimulus": self.stimulus,
				"delay_ms": self.delay # delay between presenting A and V
				}

		stimList = data.createFactorialTrialList(factors)

		randSample = random.sample(stimList, self.numTrials)
		return randSample


	
	def run_experiment(self, window_dim=[800, 600], screen_index=0, monitor_name="testMonitor"):
		""" The main function that performs the stimulus presentation with synchronized timing

		Args:
		----
		window_dim, screen_index, monitor_name: size, index, and name of stim presentation monitor. (see PsychoPy Window documentation for specifics)


		Note:
		----
		- make sure to set SYN_CONNECTED = True when actually connected to Synapse

		- to make sure the code runs smoothly, best to comment out all print statements before running an experiment 

		"""

		if(self.SYN_CONNECTED):
			# Connect to Synapse & switch to preview mode
			syn = synex.syn_connect('192.168.1.37')

		#defining the window
		window=visual.Window(size=window_dim, 
			screen=screen_index, 
			monitor=monitor_name, 
			color=[-1,-1,-1], 
			units='pix'
		)

		#instantiate a generic flash stimulus; will set the specifics of the parameters (pres_dur, luminance) later in the loop.
		flash = fs2.Flash_Stim(cur_screen=screen_index, cur_monitor=monitor_name, win_dim=window_dim, pres_dur=0, luminance=0)
		marker = pdm.PhotodiodeMarker()

		#making experimentHandler, and trials from rand_trials_sample
		trials_subset = self.rand_trials_sample()

		"""
		data_info={"ISI": 's',
				"flash_dur": 'ms',
				"luminance": 'RGB ranging from -1 (black) to 1 (white)',
				"wave_freq": 'hz', #waveFreq = freq of the tone
				"pulse_dur": 'ms', #pulseDur = length of time the tone is played
				"wave_amp": 'dB', #waveAmp = sound levels
				"stimulus": '0 (A only), 1 (V only) , or 2 (A+V)',
				"delay": 'ms' # delay between presenting A and V
				}
		"""

		exp = data.ExperimentHandler(name='testExp', savePickle=True, saveWideText=True, dataFileName='experiment')

		trials = data.TrialHandler(trialList=trials_subset, nReps=1, method='sequential') # since already randomized we can go ahead and use "sequential" here...

		exp.addLoop(trials)

		#load values into the buffer before the trial starts...
		params_list = synex.get_params(trials)
		
		if(self.SYN_CONNECTED):
			syn.setMode(3) # switch to record mode
	#	event.waitKeys(keyList='space') #could put this in to have the actual experiment (1st pdm flash, etc.) start on keypress


		expClock = core.Clock()
		expClock.reset()

		#the experiment loop! 0: Auditory only; 1: Visual only; 2: A+V
		for trial in trials:

			inter=trial['ISI_s']

			#initial marker flash for each trial
			for n in range(0, 10): #draw for 10 frames
				marker.draw_marker(window)
					
			window.flip()

			"""
			#print("Waiting system delay time...", self.SYSTEM_DELAY, " ms \n")
			time.sleep(self.SYSTEM_DELAY/1000.0)
			 
			#maximum delay if presenting auditory before visual plus maybe 30-50% ~250ms + 125 = 375ms
			sleep_time = (self.JITTER*1.5)/1000.0
			time.sleep(sleep_time) 

			"""

			stim_code = trial['stimulus']

			if(self.SYN_CONNECTED):
				#set the auditory value decided by Psychopy in Synapse: WaveAmp, WaveFreq, Delay (?)
				synex.set_stim_params(params_list, syn, trials.thisTrialN) 
				synex.set_schmitt(syn, lockout_time=self.SYSTEM_DELAY) # set the system delay lockout time 
				synex.set_stimcode(syn, stim_code)

			if(stim_code == 0 or stim_code == 2): #auditory stim only || A+V 
				core.wait((self.JITTER + self.SYSTEM_DELAY)/1000.0)

			elif(stim_code == 1):#visual stim only
				core.wait(self.JITTER/1000.0)		


			if(stim_code==0): #auditory stim only
				#print("=============================\n")
				#print("===Auditory component only===\n *Play tone at %d dB*\n" %trial['wave_amp_dB'])
				trial['delay_ms'] = None #set all visual parameters to None
				trial["flash_dur_ms"] = None
				trial["luminance"] = None 
				trial['delay_ms'] = None
				#wait while the audio is playing
				exp.addData('Aud_onset', expClock.getTime())
				core.wait(trial['pulse_dur_ms']/1000.0)
				


			elif(stim_code==1): #visual stim only 

				trial['wave_freq_Hz'] = None
				trial['pulse_dur_ms'] = None
				trial['wave_amp_dB'] = None
				trial['delay_ms'] = None  # set all audio-related parameters to none 

				if(self.SYN_CONNECTED):
					#set the auditory value decided by Psychopy in Synapse: WaveAmp, WaveFreq, Delay (?)
					syn.setParameterValue('aStim2', 'WaveAmp', 0) # set all values to 0  bc no auditory
					syn.setParameterValue('aStim2', 'WaveFreq', 0)
					syn.setParameterValue('aStim2', 'PulseDur', 0)

				#print("===========================\n")
				#print("===Visual component only===\n")
				dur = (trial['flash_dur_ms'])/1000.0 #pres. dur. in ms -> div by 1000 since flash takes in seconds
				lum = trial['luminance'] # luminance

				flash.pres_dur=dur
				flash.luminance=lum

				#print("Luminance: ", lum)
				#present the stimulus
				exp.addData('Vis_onset', expClock.getTime()) #record visual onset time

				marker.draw_marker(window)
				flash.flash(window)
				window.flip()


			elif(stim_code==2): #A+V stim
				#option 1: Audio first: delay -
				if(trial['delay_ms'] < 0): #delay = time (ms) between A and V within the trial
					#print("=================================================\n")
					#print("===Auditory and visual components on: A first ===\n *Play tone at %d dB*\n" %trial['wave_amp_dB'])

					# add auditory onset data
					exp.addData('Aud_onset', expClock.getTime())

					# wait while the audio is going + the delay btw stimuli
					total_wait = (abs(trial['delay_ms'])+trial['pulse_dur_ms'])/1000.0
					#print("Waiting for tone to play: " ,trial['pulse_dur_ms'] , "ms")
					#print("Waiting (stimulus delay): " ,(trial['delay_ms']), " ms")

					core.wait(total_wait)


					dur = (trial['flash_dur_ms'])/1000.0 #pres. dur. in ms
					lum = trial['luminance'] # luminance

					flash.pres_dur=dur
					flash.luminance=lum


					#print("Luminance: \n", lum)
					# Record visual onset
					exp.addData('Vis_onset', expClock.getTime())

					#present the stimulus
					marker.draw_marker(window)
					flash.flash(window)
					window.flip() #TODO: change to be timed by frame instead of seconds
			

				#option 2: Visual first: delay +
				if(trial['delay_ms'] > 0):
					#print("=================================================\n")
					#print("===Auditory and visual components on: V first ===\n *Play tone at %d dB*\n" %trial['wave_amp_dB'])
					dur = (trial['flash_dur_ms'])/1000.0 #pres. dur. in ms
					lum = trial['luminance'] # luminance

					flash.pres_dur=dur
					flash.luminance=lum


					#print("Luminance: \n", lum)
					exp.addData('Vis_onset', expClock.getTime()) # visual onset data

					#present the stimulus
					marker.draw_marker(window)
					flash.flash(window)
					window.flip() #TODO: change to be timed by frame instead of seconds

					#convert delay to seconds
				#	total_wait = (trial['delay_ms']+trial['pulse_dur_ms'])/1000.0 # after visual presented, need to wait the delay btw stimuli + the duration of the audio pulse
					#print("Waiting (stimulus delay): " ,trial['delay_ms'], " ms")
					core.wait(trial['delay_ms']/1000.0)

					exp.addData('Aud_onset', expClock.getTime())

					#print("Waiting for tone to play: " ,trial['pulse_dur_ms'], "ms")
					core.wait(trial['pulse_dur_ms']/1000.0)


				#option 3: Simultaneous: delay 0 
				if(trial['delay_ms'] == 0):
					#print("======================================================\n")
					#print("===Auditory and visual components on: Simultaneous ===\n *Play tone at %d dB*\n" %trial['wave_amp_dB'])
					dur = (trial['flash_dur_ms'])/1000.0 #pres. dur. in ms
					lum = trial['luminance'] # luminance

					flash.pres_dur=dur
					flash.luminance=lum

					#print("Luminance: \n", lum)

					exp.addData('Aud_onset', expClock.getTime())
					exp.addData('Vis_onset', expClock.getTime())

					#present the stimulus
					marker.draw_marker(window)
					flash.flash(window)
					window.flip() #TODO: change to be timed by frame instead of seconds

			#print("Waiting ISI Time: ", inter, 's \n')
			core.wait(inter-(self.JITTER/1000.0)) #inter stimulus interval = time between successive presentations
			window.flip()

			exp.nextEntry()


def main():


	#Parameters:
	numTrials = 10
	ISI = [2.0, 3.0, 4.0, 5.0] #ISI in seconds: time between trials
	delay = [1.0, 40.0, 80.0, 120.0, 160.0, 200.0, 240.0, -1.0, -40.0, -80.0, -120.0, -160.0, -200.0, -240.0] # *in ms -> gets converted to s in the code* ; time between presentation of A + V within a trial. (-) A first, (+) V first 


	#flash parameters
	flash_dur = [400.0, 200.0, 300.0, 50.0] #flash durs in ms 
	luminance = [[1,1,1], [.86, .86, .86], [0,.1,1]] #white , grayish, purple just for testing

	#auditory parameters: input them as the actual desired unit (Hz, ms, dB) -> will get converted if needed within the code.
	frequency = [1.1, 2.2, 3.3, 4.4] #Hz; waveFreq in TDT
	duration = [50.0, 100.0, 200.0, 300.0, 400.0] # in ms; pulseDur in TDT
	sound_levels = [15.0, 20.0, 25.0, 35.0, 55.0, 65.0] # dB; waveAmp in TDT

	stims={ 0: "auditory_only", 
			1: "visual_only",
			2: "A+V"
		}		

	exper = Experiment(numTrials=numTrials, ISI=ISI, flash_dur=flash_dur, luminance=luminance, wave_freq=frequency,pulse_dur=duration, wave_amp=sound_levels, stimulus=stims, delay=delay, SYN_CONNECTED=False)
	exper.run_experiment()

if __name__ == '__main__':
	main()






