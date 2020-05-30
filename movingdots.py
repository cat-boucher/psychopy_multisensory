from psychopy import visual, core, monitors 
import PhotodiodeMarker as pdm


class Moving_Dots():

	def __init__(self,cur_screen=0, cur_monitor="testMonitor", win_dim = [800,600], dot_size=20, num_dots=10, pres_time=20, dot_life=20, dot_speed=0.5, dot_coherence=0.5, dot_dir=90): # pres_time is time in seconds
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
		self.dot_life = dot_life
		self.dot_speed=dot_speed
		self.dot_coherence=dot_coherence
		self.dot_dir = dot_dir


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
			dotLife=self.dot_life,
			signalDots='same'

			)

		marker=pdm.PhotodiodeMarker()
	
		total_frames = self.pres_time*60 # total number of frames we need to present (assuming 60Hz monitor)

		frameN=0
		while(frameN < total_frames): 
			stimulus.draw()
			marker.draw_marker(self.mywin)
			self.mywin.flip()
			frameN += 1


		self.mywin.close()





def main():
	md = Moving_Dots()
	md.make_dots()

if __name__ == '__main__':
	main()