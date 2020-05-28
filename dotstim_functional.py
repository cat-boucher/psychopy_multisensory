from psychopy import visual, core, monitors # import libraries from Psychopy
import numpy as np
import random as rand

class Flicker_Dots():

	def __init__(self,cur_screen=0, cur_monitor="testMonitor", win_dim = [800,600], dot_size=10, num_dots=10, flicker_freq=100, pres_time=10): #flicker_freq is in Hz, pres_time is time in seconds
		self.mywin = visual.Window(size=win_dim, screen=cur_screen, monitor=cur_monitor, color=[0,0,0], units='pix') #screen can be a different # if there are >1 screen being presented
		self.dot_size=dot_size # size of dots (all uniform size)
		self.num_dots=num_dots # number of dots to be displayed
		self.pres_time=pres_time

		self.flicker_freq = flicker_freq #frequency in Hz


	def make_dots(self):
	#	mywin = visual.Window(size=self.win_dim, screen=self.cur_screen, monitor=self.cur_monitor, color=[0,0,0], units='pix')
		stimulus = visual.DotStim(
			win=self.mywin,
			units='pix',
			dotSize=self.dot_size,
			fieldSize=(800,800), #size of the field, in pixels
			nDots=self.num_dots, #number of dots that will be presete
			dir=0,
			coherence=1
			)

		clock=core.Clock()
		
		flicker_frames = 60.0/self.flicker_freq # number of frames we need each flicker to last to get the desired frequency

		frameN=0

		while clock.getTime() < self.pres_time:
			if(frameN%(2*self.flicker_freq))<self.flicker_freq: # to draw the stimulus when the frame is a multiple 
				stimulus.draw()
			self.mywin.flip()
			frameN+=1
		#core.wait(5)





def main():
	d = Flicker_Dots()
	d.make_dots()
	#mywin = visual.Window(size=[800,600], screen=0, monitor="testMonitor", color=[0,0,0], units='pix')

if __name__ == '__main__':
	main()