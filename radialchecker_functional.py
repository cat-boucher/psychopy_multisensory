from psychopy import visual, core, monitors # import libraries from Psychopy
import numpy as np

#this stimulus draws a circular, radial checkerboard on the screen

class Radial_Checkerboard():

	#cur_screen, cur_monitor, win_dim are parameters for visual.Window
	def __init__(self, cur_screen=0, cur_monitor = "testMonitor", win_dim =[800,600], stim_dur=5, stim_width=400):

		self.mywin = visual.Window(size=win_dim, screen=cur_screen, monitor=cur_monitor, color=[0,0,0], units='pix') # define the window for the stimulus to be drawn onto 
		self.stim_dur = stim_dur
		self.stim_width=stim_width


	def make_radial(self):
		stimulus = visual.RadialStim(win=self.mywin, size=(self.stim_width,self.stim_width), angularCycles=12, radialCycles=4) # i think angular=12, radial=4 looks fairly good/balanced; increase to get more (smaller) squares

		numFrames = self.stim_dur*60 #multiply stim_dur (seconds) by 60 to get number of frames we need to present the stimulus for (assuming 60 Hz monitor)

		for frame in range(numFrames):
			stimulus.draw()
			self.mywin.flip()


def main():
	rad = Radial_Checkerboard()
	rad.make_radial()

if __name__ == '__main__':
	main()