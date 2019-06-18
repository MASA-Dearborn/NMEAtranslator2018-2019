from enum import Enum #imports the enum module
import serial #importing pyserial to read the data from the Eggfinder
import threading #import threading for the buffer

class recievable(Enum): #the set of all recievable values
    NO_EGGFINDER = 0 #no eggfinder recieving
    NO_SATELLITE = 1 #no satellite recieiving
    ALL_GOOD = 2 #everything's good
i = True #the switch variable for the inifinte loop
serialAmount = 1 #the number of running serial lines

#All of the info for serial one
serialOne = serial.Serial('/dev/cu.SLAB_USBtoUART', 9600, timeout=1) #this is the
#adafruit cable, open up serial, 9600 baud rate, timeout after 1 second
rawNameOne = 'rawLog1' #the names of the logs
transNameOne = 'translatedLog1'
recievingOne = recievable(0) #the actual recieving value
bufferOne = [] #the buffer for the incoming data of one

if serialAmount == 2:
    #All of the info for serial two, only applicable if serialAmount is 2
    serialTwo = serial.Serial('/dev/cu.usbserial', 9600, timeout=1) #this is the
    #Eggfinder cable, open up serial, 9600 baud rate, timeout after 1 second
    rawNameTwo = 'rawLog2'
    transNameTwo = 'translatedLog2'
    recievingTwo =  recievable(0) #the actual recieving value
    bufferTwo = [] #the buffer for the incoming data of two

def collectData(ser, buffer):
    #the function that collects the raw data from the serial line and saves
    #it to the buffer
    raw = str(ser.readline()) #read one line of data
    length = len(raw) #obtains length of the raw data
    raw = raw[2:length-5] #removes the b' and \r\n' added bits from the raw
    #data
    buffer.append(raw) #appends the data to the buffer

def gpsRecieve(idata):
    #the function that checks whether we are recieving actual gps data
    if '$GPRMC' in idata:
        if idata.split(',')[2] == 'V':
            return recievable(1)
        if idata.split(',')[2] == 'A':
            return recievable(2)
    if '$GPGSA' not in idata or '$GPGGA' not in idata:
        return recievable(0)

def gpsCoord(idata):
    #the function that reads the GPS coordinates from the NEMA data and prints
    #as coordinates google maps can read
    if '$GPRMC' in idata or '$GPGGA' in idata:
        if '*' in idata:
            wdata = idata.split(',')
            if '$GPRMC' in idata:
                lat = [wdata[3][0:2], wdata[3][2:], wdata[4]]
                lon = [wdata[5][0:3], wdata[5][3:], wdata[6]]
            if '$GPGGA' in idata:
                lat = [wdata[2][0:2], wdata[2][2:], wdata[3]]
                lon = [wdata[4][0:3], wdata[4][3:], wdata[5]]
            return [' '.join(lat), ' '.join(lon)]


def gpsTime(idata):
    #the function that reads the time from the NEMA data and prints it as a UTC
    #timestamp
    if '$GPRMC' in idata or '$GPGGA' in idata:
        wdata = idata.split(',')[1]
        wdata = [wdata[0:2], wdata[2:4], wdata[4:6]]
        return ':'.join(wdata)

def saveData():
    #the function that saves the data to text files
    global bufferOne, recievingOne, rawNameOne, transNameOne, bufferTwo, recievingTwo, rawNameTwo, transNameTwo
    #all of the global variables

    if bufferOne != []: #if there is something in buffer one
        rawDataOne = bufferOne.pop(0)
        file = open(rawNameOne + '.txt', 'a') #creates a file called rawNameOne
        #and writes the data to it
        file.write(rawDataOne + '\n')
        file.close()

        recievingOne = gpsRecieve(rawDataOne) #testing to see if we're recieving data

        if recievingOne == recievable(2):
            file = open(transNameOne + '.txt', 'a' )#creates a file called
            #transNameOne and writes the data to it
            file.write(gpsTime(rawDataOne) + '\n')
            file.write(gpsCoord(rawDataOne)[0] + '\n')
            file.write(gpsCoord(rawDataOne)[1] + '\n')
            file.close()

    if serialAmount == 2 and bufferTwo != []: #if the second line is enabled
    #and there is something in buffer bufferTwo
        rawDataTwo = bufferTwo.pop(0)
        file = open(rawNameTwo + '.txt', 'a') #creates a file called rawNameTwo
        #and writes the data to it
        file.write(rawDataTwo + '\n')
        file.close()

        recievingTwo = gpsRecieve(rawDataTwo) #testing to see if we're recieving data

        if recievingTwo == recievable(2):
            file = open(transNameTwo + '.txt', 'a' )#creates a file called
            #transNameTwo and writes the data to it
            file.write(gpsTime(rawDataTwo) + '\n')
            file.write(gpsCoord(rawDataTwo)[0] + '\n')
            file.write(gpsCoord(rawDataTwo)[1] + '\n')
            file.close()

if __name__ == '__main__':
    serialOne.name = '/dev/cu.usbserial'
    print(serialOne.name) #make sure the serial is the right serial

    if serialAmount == 2:
        print(serialTwo.name)

    while i == True:
        #the iteration loop -- anything in here repeats forever

        #defines the threads to run
        collectThreadOne = threading.Thread(target=collectData, args=(serialOne,
        bufferOne))
        saveThread = threading.Thread(target=saveData, args=())
        if serialAmount == 2: #if there are two serial lines, run this
            collectThreadTwo = threading.Thread(target=collectData, args=(
            serialTwo, bufferTwo))

        collectThreadOne.start() #runs the threads
        saveThread.start()
        if serialAmount == 2: #if there are two serial lines, run this
            collectThreadTwo.start()

        collectThreadOne.join()
        saveThread.join()
        if serialAmount == 2: #if there are two serial lines, run this
            collectThreadTwo.join()
