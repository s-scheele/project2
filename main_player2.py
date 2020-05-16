from time import sleep
import paho.mqtt.client as mqttClient
from rpi_TM1638 import TMBoards
import board
import digitalio
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import adafruit_ssd1306
from gpiozero import LED, Button

#Setup our GPIO pins
#LED and Buttons on breadboard:

led_yes = LED(21)
led_enter = LED(16)
led_no = LED(1)

button_yes = Button(20)
button_enter = Button(12)
button_no = Button(7)

#LED with button

STB = 14
CLK = 15
DIO = 18

TM = TMBoards(DIO, CLK, STB, 0)
TM.clearDisplay()

#OLED

WIDTH = 128
HEIGHT = 32
BORDER = 5
oled_reset = digitalio.DigitalInOut(board.D4)
spi = board.SPI()
oled_cs = digitalio.DigitalInOut(board.D5)
oled_dc = digitalio.DigitalInOut(board.D6)
oled = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, oled_dc, oled_reset, oled_cs)

#OLED Textbox setup function

def oled_write(value):

    oled.fill(0)
    oled.show()

    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
    draw.rectangle(
        (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
        outline=0,
        fill=0)

    font = ImageFont.load_default()
    text = value
    (font_width, font_height) = font.getsize(text)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
        text,
        font=font,
        fill=255,
        color="red"
    )
    oled.image(image)
    oled.show()

# MQTT setup. Test server, silas/test topic.

def mqtt_write(value):
    def on_connect(client, userdate, flags, rc):

        if rc == 0:

            global Connected
            Connected = True

        else:

            print("Connection failed")


    Connected = False

    broker_address = "test.mosquitto.org"
    port = 1883
    client = mqttClient.Client("Silas")
    client.on_connect = on_connect
    client.connect(broker_address, port=port)
    client.loop_start()
    client.publish("silas/test", value)

#LEDButton Setup 
num_left = 1234
num_right = 5678

def num_update():
    TM.segments[0] = "{:04d}".format(abs(num_left)%10000)
    TM.segments[4] = "{:04d}".format(abs(num_right)%10000)

def button_led_update():
    led_enter.off()
    for i in range(8):
        TM.leds[i] = True if TM.switches[i] else False
    num_update()
    keep_going = 0
    while keep_going == 0:
        if TM.switches[0]:
            output = "Pushups"
            keep_going = 1
        if TM.switches[1]:
            output = "Crunches"
            keep_going = 1
        if TM.switches[2]:
            output = "Bicycle Crunches"
            keep_going = 1
        if TM.switches[3]:
            output = "Lunges"
            keep_going = 1
        if TM.switches[4]:
            output = "Squats"
            keep_going = 1
        if TM.switches[5]:
            output = "High Knees"
            keep_going = 1
        if TM.switches[6]:
            output = "Burpees"
            keep_going = 1
        if TM.switches[7]:
            output = "Pullups"
            keep_going = 1
    TM.clearDisplay()
    return output

def mqtt_receive_start():

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("silas/test")

    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        status = 1
        if ("silas/test" in msg.topic):
            if ("enter" in str(msg.payload)):
                led_enter.on()
                button_yes.wait_for_press()
                client.publish("silas/test", "yes")
                client.disconnect()

    client = mqttClient.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("test.mosquitto.org", 1883, 60)

    client.loop_forever()


def mqtt_receive_accept():

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("silas/test")

    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        status = 1
        if ("silas/test" in msg.topic):
            if ("yes" in str(msg.payload)):
                led_yes.on()
                client.disconnect()
            if ("no" in str(msg.payload)):
                led_no.on()
                oled_write("You win!")
                exit()
    client = mqttClient.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("test.mosquitto.org", 1883, 60)

    client.loop_forever()


def countdown():
    for i in range(10, 0, -1):
        oled_write(str(i))
        sleep(1)
    oled_write("WORKOUT")
    led_yes.off()

def workout_countdown():
    for i in range(30,9,-1):
        string = "00" + str(i)
        num_right = int(string)
        num_left = int(string)
        TM.segments[0] = "{:04d}".format(abs(num_left)%10000)
        TM.segments[4] = "{:04d}".format(abs(num_right)%10000)
        sleep(1)
    for i in range(9,0,-1):
        string = "000" + str(i)
        num_right = int(string)
        num_left = int(string)
        TM.segments[0] = "{:04d}".format(abs(num_left)%10000)
        TM.segments[4] = "{:04d}".format(abs(num_right)%10000)
        sleep(1)

def main():
    mqtt_receive_start()
    output = button_led_update()
    oled_write(output)
    mqtt_write(output)
    mqtt_receive_accept()
    while True:
        countdown()
        workout_countdown()
        mqtt_receive_accept()
        another_status = 1
        while another_status == 1:
            if button_yes.is_pressed:
                mqtt_write("yes")
                another_status = 0
            if button_no.is_pressed:
                mqtt_write("no")
                oled_write("You lose!")
                exit()



main()


