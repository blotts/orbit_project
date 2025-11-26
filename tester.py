import numpy as np

state = [1, 2, 3, 4, 5, 6]
r = np.array(state[:3])
v = np.array(state[3:])
print(r)
print(v)

state_new = np.concatenate([r, v])
xs = np.zeros(len(state_new))
ys = np.zeros(len(state_new))
xs[0], ys[0] = r[:2]
print(xs)
print(ys)