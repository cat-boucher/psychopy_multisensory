from psychopy import visual, core, monitors  # import some libraries from PsychoPy
import numpy as np

class Plaids():

	#plaids = basically 2 gratings, one on top of the other.

	#spatial_freq1, spatial_freq2, = spatial frequencies of each grating
	#ori1 = orientation of the first grating; ori2 = orientation of the second
	#opac1  =opacity of the first grating; opac2 = opacity of the 2nd grating. 
	#freq1, freq2 = frequency of the first ad 2nd grating (speed of their movement)

	def __init__(self, cur_screen=0, cur_monitor="testMonitor", win_dim=[800,600], spatial_freq1=.01, spatial_freq2=.01, ori1=0, ori2=90, opac1=1.0, opac2=0.5, text='sqr', grating1_size=800, grating2_size=800, phase=(0.0,0.0), pres_dur=5, freq1=2.0, freq2=1.0): 
		self.mywin=visual.Window(
			size=win_dim, 
			screen=cur_screen, 
			monitor=cur_monitor,
			color=[0, 0, 0],
			units="pix", 
		)
		#these are attributes for drawing the grating
		self.spatial_freq1=spatial_freq1 # spatial frequency
		self.spatial_freq2=spatial_freq2 
		self.ori1=ori1 # #orientation (in degrees clockwise from North)
		self.ori2=ori2  
		self.opac1=opac1 # opacity
		self.opac2=opac2 
		self.text=text # texture (probably best to be same for both gratings?) change to sin for fuzzy 
		self.grating1_size=grating1_size 
		self.grating2_size=grating2_size 
		self.phase = phase #

		#these are for timing the grating
		self.pres_dur=pres_dur
		self.freq1= freq1 # set both freqs to 0 for stationary picture
		self.freq2 = freq2 
		# grating frequencies (freq1, freq2) : (- -) = left and up ||  (- +) = left and down || (+ +) = right and down || (+ - ) = right and up


	def draw_plaids(self):

		#note that because of window flipping, grating2 is "on top" so keep this in mind when setting its attributes (especially opacity -- it should be less opaque)

		grating1 = visual.GratingStim(win=self.mywin, tex=self.text, units='pix', phase=self.phase, size=self.grating1_size, sf=self.spatial_freq1, ori=self.ori1, opacity=self.opac1)
		grating2 = visual.GratingStim(win=self.mywin, tex=self.text, units='pix', phase=self.phase, size=self.grating2_size, sf=self.spatial_freq2, ori=self.ori2, opacity=self.opac2)

		clock = core.Clock()
		t=0

		while t<self.pres_dur:
			t = clock.getTime()
		
			grating1.setPhase(self.freq1*t)
			grating2.setPhase(self.freq2*t)
			grating1.draw()
			grating2.draw()
			self.mywin.flip()

		self.mywin.close()


def main():
	p=Plaids()
	p.draw_plaids()

if __name__ == '__main__':
	main()
