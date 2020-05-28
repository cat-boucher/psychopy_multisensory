from psychopy import visual, core, monitors # import libraries from Psychopy
import numpy as np

class Checkerboard():

#this stimulus draws a checkerboard on the screen
#cur_screen, cur_monitor, win_dim are parameters for visual.Window
#NUM_REPEAT is the number of BW repeat squares (NUM_REPEAT*2 = num squares per row/col)
#checkerboard_width = nxn pixels in the checkerboard
#pres_dur = duration of presentation in frames
#flash_time = time each flash will last


	def __init__(self, cur_screen=0, cur_monitor = "testMonitor", win_dim = [800,600], NUM_REPEAT=10, checkerboard_width=800, pres_dur = 10, flash_time = 0.5, flash_freq=20):

		self.NUM_REPEAT = NUM_REPEAT
		self.checkerboard_width = checkerboard_width
		self.pres_dur = pres_dur
		self.flash_time = flash_time
		self.mywin = visual.Window(size=win_dim, screen=cur_screen, monitor=cur_monitor, color=[0,0,0], units='pix') #screen can be a different # if there are >1 screen being presented
		self.flash_freq=flash_freq

	def make_checkerboard(self):

		#creating the checkerboard using numpy array
		#defining black and white RGB values
		BLACK = [-1.0, -1.0, -1.0] 
		WHITE = [1.0, 1.0, 1.0]

		#create a row starting w/black and a row starting w/white, and then repeat them
		black_first = [BLACK, WHITE]
		white_first = [WHITE, BLACK]

		row_1 = black_first*self.NUM_REPEAT 
		row_2 = white_first*self.NUM_REPEAT

		arr = [row_1, row_2]
		arr = arr*self.NUM_REPEAT

		checkerboard = np.array(arr)

		stimulus = visual.ImageStim(win=self.mywin, image=checkerboard, colorSpace='rgb', size=(self.checkerboard_width, self.checkerboard_width), pos=(0, 0)) 

		#60 Hz monitor
		#loop to flash the checkerboard at the rate specified by flash_freq
		frameN=0
		numFrames = self.pres_dur*60 #pres_dur is in seconds. Multiply by 60 to get how many frames we need to present the stimulus for (assuming 60hz monitor.)

		while frameN<=numFrames: 
			if frameN % (2*self.flash_freq) < self.flash_freq:
				stimulus.draw()
			self.mywin.flip()
			frameN += 1


def main():
	c = Checkerboard()
	c.make_checkerboard()

if __name__ == '__main__':
	main()





