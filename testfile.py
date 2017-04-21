import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

t = np.linspace(-np.pi, np.pi, 1000)

x1 = np.sin(2*t)
x2 = np.cos(2*t)
x3 = x1 + x2

fig = plt.figure(figsize=(10,8))
gs = gridspec.GridSpec(2,2)

ax1 = plt.subplot(gs[0,0])
ax2 = plt.subplot(gs[0,1])
ax3 = plt.subplot(gs[1,:])

ax1.plot(t, x1, linewidth=2)
ax1.set_title('にほんごテスト')
ax1.set_xlabel('t')
ax1.set_ylabel('x')
ax1.set_xlim(-np.pi, np.pi)
ax1.grid(True)

ax2.plot(t, x2, linewidth=2)
ax2.set_title('cos')
ax2.set_xlabel('t')
ax2.set_ylabel('x')
ax2.set_xlim(-np.pi, np.pi)
ax2.grid(True)

ax3.plot(t, x3, linewidth=2)
ax3.set_title('sin+cos')
ax3.set_xlabel('t')
ax3.set_ylabel('x')
ax3.set_xlim(-np.pi, np.pi)
ax3.grid(True)

plt.show()