from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np
 
# plt.pie(
#     (10,5,10),
#     labels=('spam','ham','qq'),
#     shadow=True,
#     # a=np.random.random(40),
#     colors = cm.Set1(np.arange(8)/8.),
#     explode=(0,0.15), # space between slices
#     startangle=90,    # rotate conter-clockwise by 90 degrees
#     autopct='%1.1f%%',# display fraction as percentage
#     )
# plt.legend(fancybox=True)
# plt.axis('equal')     # plot pyplot as circle
# plt.tight_layout()
# plt.show()
labels = 'Frogs', 'Hogs', 'Dogs', 'Logs', 'ww'
sizes = [15, 30, 45, 10, 10]
explode = (0, 0.1, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()