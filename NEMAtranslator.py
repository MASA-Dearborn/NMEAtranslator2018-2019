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

def gpsRecieve(n):
    #the function that checks whether we are recieving actual gps data
    global recieving #sets up the function to work with the globabl variable
    if '$GPRMC' in data[n]:
        if data[n].split(',')[2] == 'V':
            recieving = recievable(1)
        if data[n].split(',')[2] == 'A':
            recieving = recievable(2)
    else:
        recieving = recievable(0)
    return recieving

def gpsCoord(n):
    #the function that reads the GPS coordinates from the NEMA data and prints
    #as coordinates google maps can read
    #n is the placement of the data
    if '$GPRMC' in data[n] or '$GPGGA' in data[n]:
        wdata = data[n].split(',')
        if '$GPRMC' in data[n]:
            lat = [wdata[3][0:2], wdata[3][2:], wdata[4]]
            lon = [wdata[5][0:2], wdata[5][2:], wdata[6]]
        if '$GPGGA' in data[n]:
            lat = [wdata[2][0:2], wdata[2][2:], wdata[3]]
            lon = [wdata[4][0:2], wdata[4][2:], wdata[5]]
        print(' '.join(lat))
        print(' '.join(lon))

def gpsTime(n):
    #the function that reads the time from the NEMA data and prints it as a UTC
    #timestamp
    if '$GPRMC' in data[n] or '$GPGGA' in data[n]:
        wdata = data[n].split(',')[1]
        wdata = [wdata[0:2], wdata[2:4], wdata[4:6]]
        print(':'.join(wdata))

gpsRecieve(0) #testing to see if we're recieving data
gpsRecieve(1)

if recieving == recievable(2):
    gpsTime(1) #calling the time function for data[1]
    gpsCoord(1) #calling the GPS coord function for data[1]
