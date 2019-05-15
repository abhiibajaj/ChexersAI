# wrap executing the game in an exec function
# user the stickyFingersIO to get input from the stdin
# user keras to apply inputs to the game
from __future__ import print_function
from subprocess import Popen, PIPE, STDOUT
import io
import time


class chexersWrapper:
    def __init__(self, on_gameover, on_turn):

        proc = Popen([
            'C:/Users/Matt/AppData/Local/Programs/Python/Python36/python.exe',
            '-m', 'referee',
            'stickyFingers',
            'stickyFingers',
            'stickyFingersIO'
        ], cwd='./', stdin=PIPE, stdout=PIPE, stderr=STDOUT, bufsize=1)

        # stickyFingersIO is the 3rd argument, therefore blue (rgb)
        colour = 'blue'
        # while the subprocess is writing to stdout
        while proc.poll() is None:
            # get a line from the stdout
            line = proc.stdout.readline()
            # print(line)
            # check if we won
            if line.startswith(b"* winner:"):
                # get the winner from stdout
                line = line[10:]
                line = line.decode('utf8')
                line = line.rstrip().lower()
                win = line == colour
                # pass to on gameover handler
                on_gameover(win)
                continue

            # if it's our move
            if line.startswith(b"IOSTATE"):
                line = line.decode('utf8')
                # get the state as a dictionary
                state = eval(line[8:])
                # pass the state to the on_turn handler
                action = on_turn(state)
                # convert action to byte
                action = "{}\n".format(str(action))
                action = bytes(action, 'utf-8')

                # write to the stdin
                proc.stdin.write(action)

                # flush it so the subprocess continues
                proc.stdin.flush()
                continue

        print("GAMEEXIT")
        # wait for the subprocess to close
        proc.wait()


def handle_gameover(victory):
    print("Did we win? ", victory)


def handle_turn(state):
    print("State: ", state)
    action = ('MOVE', ((2, 1), (1, 1)))
    return action


chexersWrapper(handle_gameover, handle_turn)
