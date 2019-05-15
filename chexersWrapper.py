# wrap executing the game in an exec function
# user the stickyFingersIO to get input from the stdin
# user keras to apply inputs to the game
from __future__ import print_function
from subprocess import Popen, PIPE, STDOUT
import io
import time


class Game:
    def __init__(self, mlfun):

        proc = Popen([
            'C:/Users/Matt/AppData/Local/Programs/Python/Python36/python.exe',
            '-m', 'referee',
            'stickyFingersJump0',
            'stickyFingersJump0',
            'stickyFingersIO'
        ], cwd='./', stdin=PIPE, stdout=PIPE, stderr=STDOUT, bufsize=1)

        # stickyFingersIO is the 3rd argument, therefore blue (rgb)
        colour = 'blue'
        count = 0
        # while the subprocess is writing to stdout
        while proc.poll() is None:
            line = proc.stdout.readline()
            line = line.decode('utf8')
            print(line)
            if line.startswith("IOSTATE"):
                print("IOSTATE")
                count += 1
                state = eval(line[8:])
                print("State: ", state)

                action = ('MOVE', ((2, 1), (1, 1)))
                if count == 2:
                    action = ('MOVE', ((0, 3), (0, 2)))
                print(count)

                # convert action to byte
                action = "{}\n".format(str(action))
                action = bytes(action, 'utf-8')
                # write to the stdin
                proc.stdin.write(action)
                # flush it so the subprocess continues
                proc.stdin.flush()

        # wait for the subprocess to close
        proc.wait()
        """
        for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
            print(line)
            if line.startswith("IOSTATE"):
                count += 1
                state = eval(line[8:])
                print("State: ", state)

                # get action from somewhere

                action = ('MOVE', ((2, 1), (1, 1)))
                # if count == 2:
                #   action = ('MOVE', ((0, 3), (0, 2)))
                print(count)
                # conert to a string
                action = "{}".format(str(action))
                # convert to bytes for proc.communicate
                action = bytes(action, 'utf-8')
                proc.stdin.write(action)
                #print(action, file=proc.stdin)
                proc.stdin.flush()
                #outs, errs = proc.communicate(input=action)
                #print(outs, errs)
                # proc.stdin.close()

        """
        """
        count = 0
        out = proc.stdout.readline()
        while out:
            line = out.decode('utf8')
            line = line.rstrip()

            print(line)

            if "IOSTATE" in line:
                count += 1
                state = eval(line[8:])
                print("State: ", state)

                # get action from somewhere
                action = ('MOVE', ((2, 1), (1, 1)))
                if count == 2:
                    action = ('MOVE', ((0, 3), (0, 2)))
                print(count)

                # conert to a string
                action = "{}".format(str(action))

                # convert to bytes for proc.communicate
                action = bytes(action, 'utf-8')

                proc.stdin.write(action)

                continue

            out = proc.stdout.readline()
        print("left loop")
        """


def mlfun():
    pass


Game(mlfun)
