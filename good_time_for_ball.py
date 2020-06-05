# screen /dev/ttyUSB0 115200
#ampy --port /dev/ttyUSB0 --baud 115200 put good_time_for_ball.py
from machine import Pin, I2C
import urequests
import ujson as json
import time
import network
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.scan()
# print(sta_if.connect('Habib', 'kendrick')) 
# print('connecting...')
# print('connected')


def get_data(parameter, weather_data):
    return weather_data['data'][0].get(parameter)

def storeDataFromAPI():
    for x in range (0,len(weatherAttributes) ):
        weatherCondition[x] = get_data(weatherAttributes[x], weatherData)
    return;

def clearDisplay(): # code to clear the display screen
    i2c.writeto(deviceAddress, bytes([0xFE]))
    i2c.writeto(deviceAddress, bytes([0x51]))
    return;

def getDataFromAPI():
    global response
    global weatherData
    response = urequests.get(url, headers=headers)
    weatherData = response.json()

    return
    
def displayData():
    byteCount = 0
    weatherCondition[0] = weatherCondition[0][:3] # decrease the length of the city name to 3 characters
    weatherCondition[2] = round(weatherCondition[2]) # round temperature and decrease length to 3
    weatherCondition[3] = weatherCondition[3] # round up rain amount and decrease the length of rain to 2 characters
    for x in range(0,len(weatherTitles)):
        byteCount += i2c.writeto(deviceAddress, weatherTitles[x])
        byteCount += i2c.writeto(deviceAddress, str(weatherCondition[x]))
    return;
        
def moveDisplayLeft():
    i2c.writeto(deviceAddress, bytes([0xFE]))
    i2c.writeto(deviceAddress, bytes([0x55]))
    return;
    
def scrollText():
    scrollCounter = 0
    while scrollCounter < (3*displayLength):
        moveDisplayLeft()
        time.sleep_ms(200)
        scrollCounter = scrollCounter + 1
    return;

def clearAndDisplay():
    clearDisplay()
    x = displayData()
    return x;

def goToSecondLine():
    i2c.writeto(deviceAddress, bytes([0xFE]))
    i2c.writeto(deviceAddress, bytes([0x45]))
    i2c.writeto(deviceAddress, bytes([0x40]))
    return;

def displayAnswer():
    if (weatherCondition[1] <= 5 and weatherCondition[2] >= 15 and weatherCondition[3] <= 1): 
        # 1. if wind is less than 5 m/s
        # 2. if the temperature is above 15 degrees celcius
        # 3. if the rate of rain is < 1 mm/hr
        goToSecondLine()
        i2c.writeto(deviceAddress, 'GO AND PLAY!!! :)')
    else:
        goToSecondLine()
        i2c.writeto(deviceAddress,'BAD CONDITIONS :(')
    return;

def displayTextToLCD():
    clearDisplay()
    displayData()
    displayAnswer()
    
def run_code():
    getDataFromAPI()
    storeDataFromAPI()    
    displayTextToLCD()
    scrollText()    

   
weatherAttributes = ['city_name','wind_spd', 'temp','precip']
weatherCondition = ['null','null','null','null'] 
weatherTitles = ['City:', ' Wind(m/s):', ' Temp:', ' Rain:']
deviceAddress = 40
displayLength = 40

    
i2c = I2C(scl=Pin(5), sda = Pin(4), freq = 50000)

i2c.scan()



url = "https://weatherbit-v1-mashape.p.rapidapi.com/current?lang=en&lon=-113.4938&lat=53.5461"
headers = {
        'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com",
        'x-rapidapi-key': "8623950a6dmsh625496159b93e42p1733c9jsnb2cd9bd0654a"
        }



#print('we here')
