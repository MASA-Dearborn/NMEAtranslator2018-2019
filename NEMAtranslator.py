#data = ['$GPGGA,233922.000,4219.1638,N,08313.9824,W,1,06,1.4,184.9,M,-34.0,M,,0000*64',
#'$GPRMC,233952.000,A,4219.1658,N,08313.9787,W,1.50,82.59,100119,,,A*46']
data = ['$GPRMC,190444.000,A,4146.6284,N,08634.7585,W,6.41,29.93,090219,,,A*48']
#this will be replaced by any data we get -- it's a string right now because
#I'm not sure how to classify the data yet, should probably write the data to a
#text file

def gpsCoord(n):
    #the function that reads the GPS coordinates from the NEMA data and prints
    #as coordinates google maps can read
    #n is the placement of the data
    if data[n][0:6] == '$GPGGA':
        lat = [str(data[n][18:20]), str(data[n][20:27])]
        lon = [str(data[n][31:33]), str(data[n][33:40])]
        print(lat[0] + ' ' + lat[1] + ' ' + data[n][28])
        print(lon[0] + ' ' + lon[1] + ' ' + data[n][41])
    if data[n][0:6] == '$GPRMC':
        lat = [str(data[n][20:22]), str(data[n][22:29])]
        lon = [str(data[n][33:35]), str(data[n][35:42])]
        print(lat[0] + ' ' + lat[1] + ' ' + data[n][30])
        print(lon[0] + ' ' + lon[1] + ' ' + data[n][43])

def gpsTime(n):
    #the function that reads the time from the NEMA data and prints it as a UTC
    #timestamp
    if data[n][0:6] == '$GPGGA' or data[n][0:6] == '$GPRMC':
        hr = str(data[n][7:9])
        min = str(data[n][9:11])
        sec = str(data[n][11:13])
        print(hr + ':' + min + ':' + sec)

gpsTime(0) #calling the time function for data[0]
gpsCoord(0) #calling the GPS coordinates function for data[0]
