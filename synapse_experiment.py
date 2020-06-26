import numpy as np
import tdt
from AV_experiment import Experiment

# create Synapse API connection
syn = tdt.SynapseAPI('192.168.1.37')

# switch into a runtime mode (Preview in this case)
if syn.getMode() < 1: syn.setMode(2)

gizmo_names = syn.getGizmoNames()

for gizmo in gizmo_names:
	params = syn.getParameterNames(gizmo)
#doesnt get all parameters from gizmos i.e. WaveFreq


# get all info on the 'WaveFreq' parameter
GIZMO = 'aStim2'
PARAMETER = 'WaveFreq'

# info = syn.getParameterInfo(GIZMO, PARAMETER)
#
# # get the array size (should be 100)
# sz = syn.getParameterSize(GIZMO, PARAMETER)
#
# # write values 1 to 50 in second half of buffer
# result = syn.setParameterValues(GIZMO, PARAMETER, np.arange(1, 51), 50)
#
# # read all values from buffer
# syn.getParameterValues(GIZMO, PARAMETER, sz)
#
# # get all info on the 'Go' parameter
# PARAMETER = 'Go'
# info = syn.getParameterInfo(GIZMO, PARAMETER)
#
# # flip the switch
# result = syn.setParameterValue(GIZMO, PARAMETER, 1)
#
# # check the value
freq = syn.getParameterValue(GIZMO, PARAMETER)
print('value =', freq)
freq = [freq]

# also verify visually that the switch slipped in the run
# time interface. This state change will be logged just
# like any other variable change and saved with the runtime
# state.

numTrials = 5 #total number of trials across stimuli
ISI = [2.0, 3.0, 4.0, 5.0]  # ISI in seconds

# flash parameters
flash_dur = [.001]  # flash durs in seconds (100 ms, 200 ms)
luminance = [[1, 1, 1], [.86, .86, .86], [0, .1, 1]]  # white , grayish, purple just for testing

# auditory parameters
duration = [.005]  # in seconds; pulseDur in TDT
sound_levels = [20.0, 40.0, 60.0, 80.0]  # dB; waveAmp in TDT

# Auditory on (T/F? if T then A+V, if F then Visual only)
stims = {0: "auditory_only",
		 1: "visual_only",
		 2: "A+V"
		 }

exper = Experiment(numTrials=numTrials, ISI=ISI, flash_dur=flash_dur, luminance=luminance, wave_freq=freq,
				   pulse_dur=duration, wave_amp=sound_levels, stimulus=stims)
exper.run_experiment()