from psychopy import visual, core, monitors

#class to draw the photodiode marker which will be used in all the stimuli

class PhotodiodeMarker():

	def __init__(self, cur_screen=0, cur_monitor="testMonitor", win_dim=[800,600], sqr_dim=50,pres_dur=None):

		self.marker_x = (win_dim[0]-sqr_dim)/2.0
		self.marker_y = -(win_dim[1]-sqr_dim)/2.0
		self.sqr_dim=sqr_dim # size of the square (px)
		self.pres_dur=pres_dur

	def draw_marker(self, window):
		marker = visual.Rect(win=window, size=self.sqr_dim, pos=(self.marker_x, self.marker_y), fillColor=[1,1,1])
		marker.draw()
		window.flip()


def main():
	mark=PhotodiodeMarker()
	mark.draw_marker()

if __name__ == '__main__':
	main()