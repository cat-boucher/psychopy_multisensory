from psychopy import visual, core, monitors # import libraries from Psychopy
import PhotodiodeMarker as pdm

# luminane https://www.psychopy.org/recipes/isoluminance.html

class Flash_Stim():

	def __init__(self, cur_screen=0, cur_monitor = "testMonitor", win_dim =[800,600], pres_dur=2, num_flashes=10, luminance=[1, 1, 1]): #pres_dur = in seconds
		self.mywin = visual.Window(
			size=win_dim, 
			screen=cur_screen, 
			monitor=cur_monitor, 
			color=[0,0,0], 
			units='pix'
		)
		self.size = win_dim 
		self.pres_dur=pres_dur #time (seconds) the stimulus will be presented
		self.luminance = luminance # btw -1 to 1, -1 = black 1 = white


	def flash(self):

		background = visual.Rect(win=self.mywin, size=self.size, fillColor=self.luminance)
		background.draw()
		self.mywin.flip()
		core.wait(self.pres_dur)


def main():
	fl = Flash_Stim()
	fl.flash()


if __name__ == '__main__':
	main()