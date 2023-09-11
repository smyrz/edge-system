import socket, sys, network
from hcsr04 import HCSR04
from time import sleep
import dht
import _thread
import microlite
from machine import Pin,PWM
import urequests as requests

distance_sensor = HCSR04(trigger_pin=13, echo_pin=15, echo_timeout_us=10000)

is_person = True
image = bytearray(9612)


model_file = open ('person_detect_model.tflite', 'rb')
model = bytearray (300568)
model_file.readinto(model)
model_file.close()
camera_triggered = False
def image_upload(buf):

    flask_url = 'http://192.168.57.48:5000/upload'
    r = requests.post(flask_url, headers = {'content-type': 'image/jpeg'}, data = buf)
    return r.json(), 200, {'Content-Type': 'application/json'}

def image_recognize():
    flask_url = 'http://192.168.57.48:5000/recognize'
    r = requests.get(flask_url)
    return r.json(), 200, {'Content-Type': 'application/json'}


def handle_output(person, notperson):
    global is_person
    if person > notperson:
        is_person = True
        print("is a person")
    else:
        is_person = False
        print("not a person")
      


def input_callback (interpreter):
    global image
    inputTensor = interpreter.getInputTensor(0)
    for i in range (0, len(image)):
        inputTensor.setValue(i, image[i])



def output_callback (microlite_interpreter):
    outputTensor = microlite_interpreter.getOutputTensor(0)
    not_a_person = outputTensor.getValue(0)
    person = outputTensor.getValue(1)
    print ("'not a person' = %d, 'person' = %d" % (not_a_person, person))
    handle_output(person, not_a_person)



def socket_client():

  try:
    global camera_triggered
    global image
    global is_person
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
    s.connect(('192.168.57.52', 10086))
    sleep(1)
    data = b'trigger'
    s.send(data)
    buf = b''
    length = s.recv(5)
    length = int(str(length, 'utf-8'))
    print(length)
    
    
    while True:
        temp = s.recv(1400)
        buf =buf + temp
        print(len(buf))
        if len(buf) == length:
            break
    image = buf
    print(len(image))
    interp = microlite.interpreter(model,136*1024, input_callback, output_callback)
    interp.invoke()
    if is_person:
        image_upload(image)
        msg = image_recognize()
        print(msg[0]['msg'])
        if msg[0]['msg'] == "familiar":
            s.send(b'familiar')
        else:
            s.send(b'stranger')
    else:
        image_upload(image)
        s.send(b'not a person')
    camera_triggered = False
    sleep(2)
    return True

  except socket.error as msg:
    print(msg)
    sys.exit(1)
  finally:
    s.close()


def distance_detect_loop():
  while True:
    global camera_triggered
    distance = distance_sensor.distance_cm()
    print('Distance:', distance, 'cm')

    if not camera_triggered and 0 < distance < 50:
      print('trigger camera')
      camera_triggered = True
      socket_client()
    sleep(2)


# def temperature_detect_loop():
#     temp_sensor = dht.DHT11(Pin(13))
#     while True:
#         try:
#             temp_sensor.measure()
#             temp = temp_sensor.temperature()
#             print('Temperature: %3.1f C' %temp)
#             sleep(2)
#         except OSError as e:
#             print()
            
            
    
    #distance sensor


def init():
    

    flash_light = PWM(Pin(4))
    
    flash_light.duty(5)
    sleep(1)
        # switch it off
    flash_light.duty(0)


    

    try:
        distance_detect_loop()
    #     _thread.start_new_thread( temperature_detect_loop, ())
    #     sleep(2)
    #     _thread.start_new_thread( distance_detect_loop, ())
    except Exception as e:
      print('exception ', e)
    finally:
      sleep(1)

