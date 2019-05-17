import datetime, time



def hoursago(howmanyhours):

    hoursago = (datetime.datetime.now() - datetime.timedelta(hours = howmanyhours))
    timeStamp = int(time.mktime(hoursago.timetuple()))

    return timeStamp


print(hoursago(0))
print(hoursago(3))

