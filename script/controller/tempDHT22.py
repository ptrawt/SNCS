import sys
import time
import Adafruit_DHT
sensor = Adafruit_DHT.DHT22
pin1 = 2
pin2 = 3
pin3 = 4
pin4 = 17

#while True:
def main():

    humidity1, temperature1 = Adafruit_DHT.read_retry(sensor, pin1)
    humidity2, temperature2 = Adafruit_DHT.read_retry(sensor, pin2)
    humidity3, temperature3 = Adafruit_DHT.read_retry(sensor, pin3)
    humidity4, temperature4 = Adafruit_DHT.read_retry(sensor, pin4)

    if humidity1 is not None and temperature1 is not None:
        output1 = ('Temperature={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature1, humidity1))
    else:
        print ('Failed to get reading. Try again!')

    if humidity2 is not None and temperature2 is not None:
        output2 = ('Temperature={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature2, humidity2))
    else:
        print ('Failed to get reading. Try again!')

    if humidity3 is not None and temperature3 is not None:
        output3 = ('Temperature={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature3, humidity3))
    else:
        print ('Failed to get reading. Try again!')

    if humidity4 is not None and temperature4 is not None:
        output4 = ('Temperature={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature4, humidity4))
    else:
        print ('Failed to get reading. Try again!')

    return (
        output1+'\n'+
        output2+'\n'+
        output3+'\n'+
        output4+'\n')


#print ('<--------------------------------->')

if __name__ == "__main__":
    main()
