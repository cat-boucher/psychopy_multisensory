from psychopy import visual, core, monitors 
import PhotodiodeMarker as pdb

class Flicker_Dots():

	def __init__(self,cur_screen=0, cur_monitor="testMonitor", win_dim = [800,600], dot_size=20, num_dots=10, flicker_freq=2, pres_time=20, dot_dir=45.0, dot_coherence=0.6, dot_speed=.2): #flicker_freq is in Hz (fps), pres_time is time in seconds
		self.mywin = visual.Window(
			size=win_dim, 
			screen=cur_screen, 
			monitor=cur_monitor, 
			color=[0,0,0], 
			units='pix'
		)
		
		self.dot_size=dot_size # size of dots (all uniform size)
		self.num_dots=num_dots # number of dots to be displayed
		self.pres_time=pres_time #time (seconds) the stimulus will be presented, total.
		self.dot_dir=dot_dir
		self.dot_coherence=dot_coherence
		self.dot_speed=dot_speed
		self.flicker_freq = flicker_freq #frequency in Hz





	def make_dots(self):
		stimulus = visual.DotStim(
			win=self.mywin,
			units='pix',
			dotSize=self.dot_size,
			fieldSize=(800,800), #size of the field, in pixels
			nDots=self.num_dots, #number of dots that will be presented
			dir=self.dot_dir,
			coherence=self.dot_coherence,
			speed=self.dot_speed,
			)

		
		flicker_mod = 60.0/self.flicker_freq # modulus number of frames we need to present each flicker to last to get the desired frequency
		total_frames = self.pres_time*60 # total number of frames we need to present

		marker=pdb.PhotodiodeMarker()

		frameN=0
		while(frameN < total_frames): 
			stimulus.setOpacity(0)
			if(frameN%(flicker_mod) == 0):
				stimulus.setOpacity(1)
			stimulus.draw()
			marker.draw_marker(self.mywin)

			self.mywin.flip()

			frameN += 1






def main():
	fd = Flicker_Dots()
	fd.make_dots()

if __name__ == '__main__':
	main()