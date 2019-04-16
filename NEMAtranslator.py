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
    if data[n][0:6] == '$GPRMC':
        if data[n][9] == 'V':
            recieving = recievable(1)
        if data[n][18] == 'A':
            recieving = recievable(2)
    else:
        recieving = recievable(0)
    return recieving


def gpsCoord(n):
    #the function that reads the GPS coordinates from the NEMA data and prints
    #as coordinates google maps can read
    #n is the placement of the data
    if data[n][0:6] == '$GPGGA':
        lat = [str(data[n][18:20]), str(data[n][20:27]), str(data[n][28])]
        lon = [str(data[n][31:33]), str(data[n][33:40]), str(data[n][41])]
        print(lat[0] + ' ' + lat[1] + ' ' + lat[2])
        print(lon[0] + ' ' + lon[1] + ' ' + lon[2])
    if data[n][0:6] == '$GPRMC':
        lat = [str(data[n][20:22]), str(data[n][22:29]), str(data[n][30])]
        lon = [str(data[n][33:35]), str(data[n][35:42]), str(data[n][43])]
        print(lat[0] + ' ' + lat[1] + ' ' + lat[2])
        print(lon[0] + ' ' + lon[1] + ' ' + lon[2])

def gpsTime(n):
    #the function that reads the time from the NEMA data and prints it as a UTC
    #timestamp
    if data[n][0:6] == '$GPGGA' or data[n][0:6] == '$GPRMC':
        hr = str(data[n][7:9])
        min = str(data[n][9:11])
        sec = str(data[n][11:13])
        print(hr + ':' + min + ':' + sec)

gpsRecieve(0) #testing to see if we're recieving data
gpsRecieve(1)

if recieving == recievable(2):
    gpsTime(1) #calling the time function for data[1]
    gpsCoord(1) #calling the GPS coord function for data[1]
