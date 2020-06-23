from psychopy import visual, core, monitors 

#updates from v1: flash now takes the window to be drawn on as input, allowing for more flexibility

class Flash_Stim():

	def __init__(self, cur_screen=0, cur_monitor = "testMonitor", win_dim =[800,600], pres_dur=2, luminance=[1, 1, 1]): #pres_dur = in seconds
		
		self.size = win_dim 
		self.pres_dur=pres_dur #time (seconds) the stimulus will be presented
		self.luminance = luminance # btw -1 to 1, -1 = black 1 = white


	#input also the window to be drawn on.
	def flash(self, window):

		background = visual.Rect(win=window, size=self.size, fillColor=self.luminance)
		background.draw()
		window.flip()
		core.wait(self.pres_dur)
		background.setOpacity(0)

	#	window.close()

def main():
	fl = Flash_Stim()
	fl.flash()


if __name__ == '__main__':
	main()