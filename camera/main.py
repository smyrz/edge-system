import machine,socket,time
import socket
import network
import camera
import urequests as requests


def image_upload(buf):

    flask_url = 'http://192.168.57.48:5000/upload'
    r = requests.post(flask_url, headers = {'content-type': 'image/jpeg'}, data = buf)
    return r.json(), 200, {'Content-Type': 'application/json'}


# deal socket
def deal_data(conn, addr):
    print('New Connection：{0}'.format(addr))
    # listen
    data = conn.recv(10240)
    data = str(data,'utf-8')
    print(data)
    
    maxcache = 1400


    if data == 'trigger':
        buf = camera.capture() # get figure
        # send to edge
        # recevie msg from edge and classify whether need more picture
        print(str(len(buf)).encode('utf-8'))

        conn.send(str(len(buf)).encode('utf-8'))
        conn.send(buf)
        is_person = conn.recv(10240)
        is_person = str(is_person,'utf-8')
        if is_person == 'not a person':
            print("not a person")
        elif is_person == 'familiar':
            print('familiar')
        elif is_person == 'stranger':
            print("stranger")
            for i in range(10):
                image_upload(camera.capture())
                time.sleep(0.5)
    conn.close()

# initial camera
def camera_init():
    camera.deinit()
    try:
        camera.init(0, format=3)
    except Exception as e:
        print('camera initial error')
        camera.deinit()
        camera.init(0, format=3)
    # figure setting 
      
    ## Other settings:
    # flip up side down
#     camera.flip(1)
    # left / right
    camera.mirror(1)
     
    # framesize
#     camera.framesize(camera.FRAME_96X96)
    camera.framesize(camera.FRAME_HVGA)

    # The options are the following:
    # FRAME_96X96 FRAME_QQVGA FRAME_QCIF FRAME_HQVGA FRAME_240X240
    # FRAME_QVGA FRAME_CIF FRAME_HVGA FRAME_VGA FRAME_SVGA
    # FRAME_XGA FRAME_HD FRAME_SXGA FRAME_UXGA FRAME_FHD
    # FRAME_P_HD FRAME_P_3MP FRAME_QXGA FRAME_QHD FRAME_WQXGA
    # FRAME_P_FHD FRAME_QSXGA
    # Check this link for more information: https://bit.ly/2YOzizz
     
    # special effects
    camera.speffect(camera.EFFECT_NONE)
    # The options are the following:
    # EFFECT_NONE (default) EFFECT_NEG EFFECT_BW EFFECT_RED EFFECT_GREEN EFFECT_BLUE EFFECT_RETRO
     
    # white balance
    camera.whitebalance(camera.WB_NONE)
    # The options are the following:
    # WB_NONE (default) WB_SUNNY WB_CLOUDY WB_OFFICE WB_HOME
     
    # saturation
    camera.saturation(0)
    # -2,2 (default 0). -2 grayscale 
     
    # brightness
    camera.brightness(0)
    # -2,2 (default 0). 2 brightness
     
    # contrast
    camera.contrast(0)
    #-2,2 (default 0). 2 highcontrast
     
    # quality
    camera.quality(10)
    # 10-63 lower number means higher quality
    print('camera init')
      
def init():
    flash_light = machine.PWM(machine.Pin(4))
    
    flash_light.duty(5)
    time.sleep(1)
    flash_light.duty(0)
    
    
    camera_init()

    # listen 10086 from all source
    ADDR = ('0.0.0.0',10086)

    # use tcp
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM, 0)

    s.bind(ADDR)
    s.listen(1)
    try:
        while True:
            print('waiting for connection...')
            # begin listen
            try:
                conn, addr = s.accept()
                deal_data(conn, addr)
            except:
                pass
            finally:
                conn.close()
    except:
        camera.deinit()



