import serial #importing pyserial to read the data from the Eggfinder
#open up Eggfinder serial, 9600 baud rate, timeout after 1 second
ser = serial.Serial('/dev/cu.usbserial', 9600, timeout=1) #this is the
#adafruit cable
print(ser.name) #make sure the serial is the right serial
rawLogName = 'rawLog'
i = True #the switch variable for the inifinte loop

def collectData():
    raw = str(ser.readline()) #read one line of data
    length = len(raw) #obtains length of the raw data
    raw = raw[2:length-5] #removes the b' and \r\n' added bits from the raw data
    return raw

while i == True:
    #the iteration loop -- anything in here repeats forever
    rawData = [collectData(), collectData(), collectData(), collectData(), collectData()]
    #collect data and set the data variable to the collected data

    file = open(rawLogName + '.txt', 'a') #creates a file called "log.txt" and writes
    #the data to it
    file.write(rawData[0] + '\n')
    file.write(rawData[1] + '\n')
    file.write(rawData[2] + '\n')
    file.write(rawData[3] + '\n')
    file.write(rawData[4] + '\n')
    file.close()
