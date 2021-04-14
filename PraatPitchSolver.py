import csv
import sys
import numpy as np

class PraatPitchSolver(object):
	def __init__(self, filename_input, filename_output):

		self.filename_input = filename_input
		self.filename_output = filename_output

	def fix_praat_pitch(self):
		"""
		This function formats the PRAAT pitch extraction output. It basically rewrites the pitch
		file into a better format for further use and evaluation of the pitch track.
		"""

		print('Fixing praat pitch file...')

		praat_timestamps = []
		new_pitch_values = []

		with open(self.filename_input, 'r') as f:
			reader = csv.reader(f, delimiter=' ')
			next(reader)
			for idx, line in enumerate(reader):
				line = [x for x in line if len(x) > 1]
				new_pitch = line[1] if line[1] != '--undefined--' else 0.0
				new_pitch_values.append(float(new_pitch))
				new_timestamp = float(line[0]) if line[1] != '--undefined--' else -1
				praat_timestamps.append(new_timestamp)

			silent_first = True if praat_timestamps[0] == -1 else False
			silent_end = True if praat_timestamps[-1] == -1 else False

			yes_to_no = []
			for i in np.arange(0, len(praat_timestamps)-1):
				if praat_timestamps[i] > 0.0 and praat_timestamps[i+1] < 0.0:
					yes_to_no.append(i)

			no_to_yes = []
			for i in np.arange(0, len(praat_timestamps)-1):
				if praat_timestamps[i] < 0.0 and praat_timestamps[i+1] > 0.0:
					no_to_yes.append(i+1)

			# First gap (if any)
			if silent_first:
				start_time = no_to_yes[0]
				no_to_yes = no_to_yes[1:]
				praat_timestamps[0: start_time+1] = np.linspace(
					0,
					praat_timestamps[start_time],
					num=start_time+1)

			# Last gap (if any)
			if silent_end:
				end_time = yes_to_no[-1]
				yes_to_no = yes_to_no[:-1]

				count = 0
				for i in reversed(praat_timestamps):
					count = count + 1
					if i > 0:
						break

				time_step = praat_timestamps[end_time-1] - praat_timestamps[end_time-2]
				for i in np.arange(1, count):
					praat_timestamps[end_time + i] = praat_timestamps[end_time] + (time_step * i)

			# Mid gaps
			for i, j in zip(yes_to_no, no_to_yes):
				praat_timestamps[i: j+1] = np.linspace(
					praat_timestamps[i],
					praat_timestamps[j],
					num=(j-i)+1)

		return praat_timestamps, new_pitch_values

	def save_pitch(self, timestamps, pitch_values):
		"""
		This function saves pich track to a formatted .txt file.
		Args:
			timestamps (list): list of timestamps
			pitch_values (list): list of pitch values
		"""

		# with open(os.path.join(os.path.dirname(filename), 'PRAAT_pitch.txt'), 'w+') as f:
		with open(self.filename_output, 'w+') as f:
			for i, j in zip(timestamps, pitch_values):
				f.write("{}, {}\n".format(i, j))
		f.close()

		print('Done!')
		print('Stored as: {}'.format(self.filename_output))


# Main
if __name__ == '__main__':

	# Initializing pitch solver
	praat_pitch_solver = PraatPitchSolver(
		filename_input=sys.argv[1],
		filename_output=sys.argv[2],
	)

	# Obtaining fixed pitch
	fixed_timestamps, fixed_pitch_values = praat_pitch_solver.fix_praat_pitch()

	# Saving fixed pitch
	praat_pitch_solver.save_pitch(
		timestamps=fixed_timestamps,
		pitch_values=fixed_pitch_values,
	)

