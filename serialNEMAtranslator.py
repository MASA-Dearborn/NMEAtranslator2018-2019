from enum import Enum #imports the enum module
import serial #importing pyserial to read the data from the Eggfinder
#import threading #import threading for the buffer

ser = serial.Serial('/dev/cu.usbserial', 9600, timeout=1) #this is the
#adafruit cable, open up Eggfinder serial, 9600 baud rate, timeout after 1 second
print(ser.name) #make sure the serial is the right serial

rawLogName = 'rawLog'
transLogName = 'translatedLog'
class recievable(Enum): #the set of all recievable values
    NO_EGGFINDER = 0 #no eggfinder recieving
    NO_SATELLITE = 1 #no satellite recieiving
    ALL_GOOD = 2 #everything's good
i = True #the switch variable for the inifinte loop
recieving = recievable(0) #the actual recieving value

def collectData():
    #the function that collects the raw data from the serial line
    raw = str(ser.readline()) #read one line of data
    length = len(raw) #obtains length of the raw data
    raw = raw[2:length-5] #removes the b' and \r\n' added bits from the raw data
    return raw

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

while i == True:
    #the iteration loop -- anything in here repeats forever
    rawData = collectData()
    #collect data and set the data variable to the collected data

    file = open(rawLogName + '.txt', 'a') #creates a file called rawLogName and writes
    #the data to it
    file.write(rawData + '\n')
    file.close()

    gpsRecieve(rawData) #testing to see if we're recieving data

    if recieving == recievable(2):
        file = open(transLogName + '.txt', 'a' )#creates a file called
        #transLogName and writes the data to it
        file.write(gpsTime(rawData) + '\n')
        file.write(gpsCoord(rawData)[0] + '\n')
        file.write(gpsCoord(rawData)[1] + '\n')
        file.close()
