# PraatPitchSolver

Python-based solution to fix PRAAT extracted pitch in macOS machines,
which sets as ```--undefined--``` the timestamps and pitch values within
the unpitched regions. This setting is quite unconvenient to work with
the extracted pitch track. PraatPitchSolver is basically written to fix that,
providing a reliable and aligned formatting for the macOS Praat pitch tracks.

---

### Running PraatPitchSolver from terminal
You can format your Praat pitch file by running the following command lines:

```
cd path/to/PraatPitchSolver
python3 PraatPitchSolver.py 'path/to/Praat/file.txt' 'path/to/output/file.txt'
```

### Running PraatPitchSolver from Python code
You would need to move PraatPitchSolver to your project file and import it:

```
from PraatPitchSolver import PraatPitchSolver

# Initialize pitch solver instance
praat_pitch_solver = PraatPitchSolver(
    filename_input='path/to/Praat/file.txt',
    filename_output='path/to/output/file.txt',
)

# Obtain fixed pitch
fixed_timestamps, fixed_pitch_values = praat_pitch_solver.fix_praat_pitch()

# Saving fixed pitch
praat_pitch_solver.save_pitch(
    timestamps=fixed_timestamps,
    pitch_values=fixed_pitch_values,
)
```

### Contact
For further question please write an email to genis.plaja01@estudiant.upf.edu.