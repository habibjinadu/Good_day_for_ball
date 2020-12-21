# screen /dev/ttyUSB0 115200
#ampy --port /dev/ttyUSB0 --baud 115200 put good_time_for_ball.py
# make sure you set serial baud rate to 115200

from machine import Pin, I2C
import urequests
import ujson as json
import time
from time import sleep
import network

def do_connect():  # connect to the internet
    import network
    # connect to the internet
    sta_if = network.WLAN(network.STA_IF) # configure the ESP8266 to enable wifi
    sta_if.active(True)                   # make it active                     
    sta_if.scan()                           # scan for available access points
    #sta_if.connect('Habib', 'kendrick')     # connect to this wifi network
    # enter in your Wi-Fi Name and Password
    while (not sta_if.isconnected()):
        sta_if.active(True)
        sta_if.connect('Habib', 'kendrick') 
        time.sleep_ms(1000)                      # wait for 200 ms
        print('connecting...')
    return sta_if.isconnected();

def get_data(parameter, weather_data): # get a specific parameter from weather_data 
    return weather_data['data'][0].get(parameter) # return the parameter at entry 0 of weather_data

def storeDataFromAPI():
    for x in range (0,len(weatherAttributes) ):         # for all weather attributes
        weatherCondition[x] = get_data(weatherAttributes[x], weatherData)  # get the API value for each weather attribute
    return;

def clearDisplay(): # code to clear the display screen
    i2c.writeto(deviceAddress, bytes([0xFE]))               # send the prefix command to the LCD
    i2c.writeto(deviceAddress, bytes([0x51]))               # send the clear screen comant to the LCD
    return;

def getDataFromAPI():
    global receivedData                                 # declare a global receivedData variable 
    global weatherData                                  # declare a global weatherData variable
    receivedData = urequests.get(url, headers=headers)  # store requested data in receivedData
    weatherData = receivedData.json()                   # organize the requested data and store it in weatherData
    return;
    
def displayData():# displays the weather data on the Line 1 of the LCD screen                                          
    byteCount = 0                                           # initialize byteCount variable to keep track of the number of bytes sent to the LCD
    weatherCondition[0] = weatherCondition[0][:3]       # decrease the length of the city name to 3 characters
    weatherCondition[2] = round(weatherCondition[2])    # round temperature and decrease length to 3
    weatherCondition[3] = weatherCondition[3]           # round up rain amount and decrease the length of rain to 2 characters
    for x in range(0,len(weatherTitles)):               
        byteCount += i2c.writeto(deviceAddress, weatherTitles[x])               # send weatherTitles to the LCD
        byteCount += i2c.writeto(deviceAddress, str(weatherCondition[x]))       # send weatherConditions for the weatherTitle to the LCD
    return byteCount;                                                               # return byteCount

def moveDisplayLeft(): # moves all characters on the LCD one space to the left     
    i2c.writeto(deviceAddress, bytes([0xFE]))       # send the prefix command to the LCD
    i2c.writeto(deviceAddress, bytes([0x55]))       # send a command that moves the display one place to the left
    return;
    
def scrollText(): # scrolls all of the characters continuously to the left
    scrollCounter = 0                               # initialize a scrollCounter variable to keep track of the amount of scrolls
    while scrollCounter < (3*displayLength):        # while scroll counter is less than 3* display length (3*40)
        moveDisplayLeft()                           # move the display
        time.sleep_ms(200)                          # wait for 200 ms
        scrollCounter = scrollCounter + 1           # increment the scrollCounter
    return;

def clearAndDisplay(): # clear the screen and display new info on the LCD
    clearDisplay()                                  # clear the display to start with a blank screen
    x = displayData()                               # display the weatherTitles and weatherConditions
    return x;

def goToSecondLine(): # go to the second line of the LCD
    i2c.writeto(deviceAddress, bytes([0xFE]))       # send the prefix command to the LCD
    i2c.writeto(deviceAddress, bytes([0x45]))       # send the 'set cursor' command to the LCD. This command needs followed with a cursor position byte
    i2c.writeto(deviceAddress, bytes([0x40]))       # set the cursor postion byte to the 1st column of Line 2 on the display
    return;

def displayAnswer(): # display the answer on Line 2 of the LCD screen
    if (weatherCondition[1] <= 5 and weatherCondition[2] >= 15 and weatherCondition[3] <= 1): 
        # 1. if wind is less than 5 m/s
        # 2. if the temperature is above 15 degrees celcius
        # 3. if the rate of rain is < 1 mm/hr
        goToSecondLine()                                            # go to the second line of the LCD
        i2c.writeto(deviceAddress, 'GO AND PLAY!!! :)')             # display "GO and PLAY!!! :)" on the second line LCD
    else:
        goToSecondLine()                                            # go to the second line of the LCD
        i2c.writeto(deviceAddress,'BAD CONDITIONS :(')              # display "BAD CONDITIONS :(" on the second line of the LCD
    return;

def displayTextToLCD(): # displayText to the LCD
    clearDisplay()                                                  # clear the LCD display        
    displayData()                                                   # displayData
    displayAnswer()                                                 # displayAnswer
    
def run_code(): 
    getDataFromAPI()        # get weatherData from the API
    storeDataFromAPI()      # store and organize data from the API in a variable    
    displayTextToLCD()      # display the text to the LCD screen
    scrollText()            # continuously move the LCD screen to the left.

   
weatherAttributes = ['city_name','wind_spd', 'temp','precip']           # create an array of weatherAttributes that will match the data from the API
weatherCondition = ['null','null','null','null']                        # create an array of weatherConditions
weatherTitles = ['City:', ' Wind(m/s):', ' Temp:', ' Rain:']            # create an array of weatherTitles that will be shown on the LCD screen
deviceAddress = 40                                                      # the address for the NHD-0216K3Z LCD is 40
displayLength = 40                                                      # the maximum display length for the LCD is 40s

    
i2c = I2C(scl=Pin(5), sda = Pin(4), freq = 50000)                       # initialize the I2C pin with where D1-GPIO5 is SCL and D2-GPIO4 is SDA, and the SCL frequency is 50 kHz (Max for the LCD is 100kHz)

#i2c.scan()                                                              # scan for available I2C devices



url = "https://weatherbit-v1-mashape.p.rapidapi.com/current?lang=en&lon=-113.4938&lat=53.5461"  # API URL
headers = {                                                                                     # API Headers      
        'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com",
        'x-rapidapi-key': "8623950a6dmsh625496159b93e42p1733c9jsnb2cd9bd0654a"
        }



#print('we here')
