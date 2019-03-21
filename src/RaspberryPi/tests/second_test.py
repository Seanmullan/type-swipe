import data
import time

data = data.Data()

data.set_proximity(15)
data.set_inductive(1000)
time.sleep(2)

data.set_proximity(3)
data.set_inductive(2000)
time.sleep(2)

data.set_proximity(15)
data.set_inductive(1000)