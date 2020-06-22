import numpy as np
import tdt

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
info = syn.getParameterInfo(GIZMO, PARAMETER)
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
# value = syn.getParameterValue(GIZMO, PARAMETER)
# print('value =', value)

# also verify visually that the switch slipped in the run
# time interface. This state change will be logged just
# like any other variable change and saved with the runtime
# state.