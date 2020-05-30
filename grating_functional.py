from psychopy import visual, core, monitors 
import PhotodiodeMarker as pdm #Photodiode marker library

class Grating():

#creating grating stimulus. sf=spatial frequency; orientation=orientation in degrees from North, 
#phase=like which "phase" of the sin wave it is in
#text (texture) = sin
#freq = n Hz -- how fast you want the grating to drift. NOTE: if -n then it will drift left

	def __init__(self, cur_screen=0, cur_monitor="testMonitor", win_dim=[800,600], spatial_freq=.01, orientation=0, text='sin', grating_size=800, phase=(0.0,0.0), pres_dur=10, freq=-2):
		self.mywin=visual.Window(
			size=win_dim, 
			screen=cur_screen, 
			monitor=cur_monitor,
			color=[0, 0, 0],
			units="pix", 
		)
		self.spatial_freq=spatial_freq # increasing sf -> smaller bars (more frequent!)
		self.orientation=orientation # in degrees (default by psychopy)
		self.text=text #texture
		self.grating_size=grating_size
		self.phase=phase
		self.freq=freq # a positive or negative float denoting the frequency at which the stimulus drifts; a - value means it drifts left, + means it drifts right
		self.pres_dur=pres_dur #in seconds


	def draw_grating(self):

		grating = visual.GratingStim(win=self.mywin, tex=self.text, units='pix', phase=self.phase, size=self.grating_size, sf=self.spatial_freq, ori=self.orientation)
	
		clock = core.Clock()
		t=0

		marker = pdm.PhotodiodeMarker()

		while t<self.pres_dur:
			t = clock.getTime()
			grating.setPhase(self.freq*t)
			grating.draw()
			marker.draw_marker(self.mywin)
			self.mywin.flip()

		self.mywin.close()



def main():
	grat=Grating()
	grat.draw_grating()

if __name__ == '__main__':
	main()