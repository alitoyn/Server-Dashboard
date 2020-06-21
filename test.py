import datetime

data = "23:47:52:WU00:FS00:0xa7:Completed 1 out of 250000 steps (0%)"
current = "12:40:39:WU00:FS00:0xa7:Completed 115000 out of 250000 steps (46%)"

data = data.split(":")
current = current.split(":")

dummydate1 = datetime.date(1994,11,16)
dummydate2 = datetime.date(1994,11,15)

time1 = datetime.time(int(data[0]), int(data[1]), int(data[2]))
time2 = datetime.time(int(current[0]), int(current[1]), int(current[2]))

diff = datetime.datetime.combine(dummydate1,time2) - datetime.datetime.combine(dummydate1,time1)
if str(diff[0]) == '-':
	diff = datetime.datetime.combine(dummydate1,time2) - datetime.datetime.combine(dummydate2,time1)

print(diff)



