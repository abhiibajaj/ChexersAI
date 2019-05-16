# wrap executing the game in an exec function
# user the stickyFingersIO to get input from the stdin
# user keras to apply inputs to the game
from __future__ import print_function
from subprocess import Popen, PIPE, STDOUT
import io
import sys


class chexersWrapper:
    def run(self, on_gameover, on_turn, on_gameerror):

        game_memory = []

        proc = Popen([
            sys.executable,
            '-m', 'referee',
            'stickyFingersUniformCost',
            'stickyFingersUniformCost',
            'stickyFingersIO'
        ], cwd='./', stdin=PIPE, stdout=PIPE, stderr=STDOUT, bufsize=1)

        # stickyFingersIO is the 3rd argument, therefore blue (rgb)
        colour = 'blue'
        win = False
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
                # pass to on gameover handler
                win = True
                on_gameover(line)
                continue

            # if it's our move
            if line.startswith(b"IOSTATE"):
                line = line.decode('utf8')
                # get the state as a dictionary
                colour, state = eval(line[8:])
                # pass the state to the on_turn handler
                action = on_turn(colour, state)

                # add it to the game memory
                game_memory.append([
                    state, action
                ])

                # convert action to byte
                action = "{}\n".format(str(action))
                action = bytes(action, 'utf-8')

                # write to the stdin
                proc.stdin.write(action)

                # flush it so the subprocess continues
                proc.stdin.flush()

                continue

        # the game ended without a winner, this is bad
        if not win:
            on_gameerror()

        # wait for the subprocess to close
        proc.wait()
        return game_memory
