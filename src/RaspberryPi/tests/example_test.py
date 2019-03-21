import data
import time

data = data.Data()

data.set_proximity(15)
data.set_inductive(1000)
time.sleep(2)

data.set_proximity(10)
data.set_inductive(100)
time.sleep(2)

data.set_proximity(15)
data.set_inductive(1000)
time.sleep(2)

data.set_proximity(10)
data.set_inductive(1000)
time.sleep(2)

data.set_proximity(15)
data.set_inductive(1000)