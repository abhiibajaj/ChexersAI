# wrap executing the game in an exec function
# user the stickyFingersIO to get input from the stdin
# user keras to apply inputs to the game

import subprocess
import io

proc = subprocess.Popen([
    'C:/Users/Matt/AppData/Local/Programs/Python/Python36/python.exe',
    '-m', 'referee',
    'stickyFingersJump0',
    'stickyFingersJump0',
    'stickyFingersIO'
], cwd='./', stdout=subprocess.PIPE)

colour = 'blue'
for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):  # or another encoding
    if line.startswith("IOSTATE"):
        state = eval(line[8:])
        for item in state.items():
            print(item)
