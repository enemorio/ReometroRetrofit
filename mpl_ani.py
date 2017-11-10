import matplotlib.pyplot as pyplot
import matplotlib.animation as animation
import random
import time

pyplot.style.use('fast')

y = []
t = []

fig = pyplot.figure()
axis0 = fig.add_subplot(1,1,1)


def refresh(i):
  y.append(time.time())   
  t.append(random.random())
  axis0.clear()
  axis0.plot(y,t)

ani = animation.FuncAnimation(fig, refresh, interval=1)
pyplot.show()	# This locks the thread
print('I ran')