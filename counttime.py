import datetime

timeList = [
    '0:09:59',
    '0:09:36',
    '0:02:09',
    '0:07:54',
    '0:06:02',
    '0:03:57',
    '0:01:46',
]
mysum = datetime.timedelta()
for i in timeList:
    (h, m, s) = i.split(':')
    d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    mysum += d
print(str(mysum))