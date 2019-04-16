import serial #importing pyserial to read the data from the Eggfinder
#open up Eggfinder serial, 9600 baud rate, timeout after 1 second
ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 9600, timeout=1) #this is the
#adafruit cable
print(ser.name) #make sure the serial is the right serial
rawLogName = 'rawLog'

def collectData():
    raw = str(ser.readline()) #read one line of data
    length = len(raw) #obtains length of the raw data
    raw = raw[2:length-5] #removes the b' and \r\n' added bits from the raw data
    return raw

data = [collectData(), collectData()] #collect data and set the data variable to
#the collected data

file = open(rawLogName + '.txt', 'a') #creates a file called "log.txt" and writes
#the data to it
file.write(data[0] + '\n')
file.write(data[1] + '\n')
file.close()
