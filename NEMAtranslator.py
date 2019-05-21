from enum import Enum #imports the enum module
class recievable(Enum): #the set of all recievable values
    NO_EGGFINDER = 0 #no eggfinder recieving
    NO_SATELLITE = 1 #no satellite recieiving
    ALL_GOOD = 2 #everything's good

data = ['$GPRMC,,V,,,,,,,,,,N*53',
'$GPRMC,185432.000,A,4146.6460,N,08634.6052,W,0.00,177.78,090219,,,A*73']
#data taken from various previous tests, will be replaced with live data in
#final program

recieving = recievable(0) #the actual recieving value

def gpsRecieve(idata):
    #the function that checks whether we are recieving actual gps data
    global recieving #sets up the function to work with the globabl variable
    if '$GPRMC' in idata:
        if idata.split(',')[2] == 'V':
            recieving = recievable(1)
        if idata.split(',')[2] == 'A':
            recieving = recievable(2)
    else:
        recieving = recievable(0)
    return recieving

def gpsCoord(idata):
    #the function that reads the GPS coordinates from the NEMA data and prints
    #as coordinates google maps can read
    if '$GPRMC' in idata or '$GPGGA' in idata:
        wdata = idata.split(',')
        if '$GPRMC' in idata:
            lat = [wdata[3][0:2], wdata[3][2:], wdata[4]]
            lon = [wdata[5][0:2], wdata[5][2:], wdata[6]]
        if '$GPGGA' in idata:
            lat = [wdata[2][0:2], wdata[2][2:], wdata[3]]
            lon = [wdata[4][0:2], wdata[4][2:], wdata[5]]
        return [' '.join(lat), ' '.join(lon)]

def gpsTime(idata):
    #the function that reads the time from the NEMA data and prints it as a UTC
    #timestamp
    if '$GPRMC' in idata or '$GPGGA' in idata:
        wdata = idata.split(',')[1]
        wdata = [wdata[0:2], wdata[2:4], wdata[4:6]]
        return ':'.join(wdata)

gpsRecieve(data[0]) #testing to see if we're recieving data
gpsRecieve(data[1])

if recieving == recievable(2):
    print(gpsTime(data[1])) #calling the time function for data[1]
    print(gpsCoord(data[1])[0]) #calling the GPS coord function for data[1]
    print(gpsCoord(data[1])[1])
