from __future__ import print_function

import random
import sys
import time

goal = random.randint(1,10)
goal = 20
for i in range(goal):
    file = random.choice((sys.stdout, sys.stderr))
    t = random.randint(1, 200) / 100.0
    print(i, goal, t, file.isatty(), file=file)
    file.flush()
    time.sleep(t)
