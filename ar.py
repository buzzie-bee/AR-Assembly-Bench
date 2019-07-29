from kivy.config import Config
screen_width = 1240
screen_height = 720
Config.set('graphics', 'resizable', '0') #0 being off 1 being on as in true/false
Config.set('graphics', 'width', str(screen_width))
Config.set('graphics', 'height', str(screen_height))

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color
from kivy.graphics import Line
from kivy.graphics import PopMatrix
from kivy.graphics import PushMatrix
from kivy.graphics import Rotate
from kivy.graphics import Rectangle

from kivy.clock import Clock

import random
import math
import numpy

class DisplayImage(Image):

    def __init__(self,image_num=1,coords=(620,360), angle=315,**kwargs):
        image = ImageProps()
        self.source=image.filename
        self.size= image.size
        self.size_hint=(None,None)
        self.allow_stretch=(True)
        self.coords = coords
        self.pos= (coords[0]-image.offset[0], coords[1] - image.offset[1])
        self.angle = angle
        print(self.pos)

        super(DisplayImage, self).__init__(**kwargs)

        with self.canvas.before:
            PushMatrix()
            Rotate(angle=angle, axis=(0,0,1), origin=self.center)

        #with self.canvas:
            #Color(1,0,0,0.5, mode='rgba')
            #Rectangle(pos=self.pos, size=(self.size))
        with self.canvas.after:
            PopMatrix()
            Color(1,0,0,1, mode='rgba')
            Line(points=image.rectangle_vertex(image_size = self.size, image_pos = self.coords, image_angle = self.angle), width=1)
            
            #center line:
            Line(points=(620,0,620,720), width=1)
            

class ImageProps():

    def __init__(self, image_number=1, scale_f=1):

        print("looking up image props")
        self.size = (100,20)
        self.offset = (self.size[0]/2,self.size[1]/2)
        #self.offset = (0,0)
        self.filename = 'keyence.png'

    def rectangle_vertex(self,image_size, image_pos, image_angle):
        #Calculates the size of the rectangular lines surrounding the components
        
        #rect scale makes rectangle x% bigger than the real part
        rect_scale = 1.2
        rect_width = (int(image_size[0] / (2/rect_scale)))
        rect_height = (int(image_size[1] / (2/rect_scale)))
        a = math.radians(image_angle)

        rect_x1 = int(image_pos[0] - (rect_width * math.cos(a)) - (rect_height * math.sin(a)))
        rect_x2 = int(image_pos[0] + (rect_width * math.cos(a)) - (rect_height * math.sin(a)))
        rect_x3 = int(image_pos[0] + (rect_width * math.cos(a)) + (rect_height * math.sin(a)))
        rect_x4 = int(image_pos[0] - (rect_width * math.cos(a)) + (rect_height * math.sin(a)))

        rect_y1 = int(image_pos[1] - (rect_width* math.sin(a)) + (rect_height * math.cos(a)))
        rect_y2 = int(image_pos[1] + (rect_width * math.sin(a)) + (rect_height * math.cos(a)))
        rect_y3 = int(image_pos[1] + (rect_width * math.sin(a)) - (rect_height * math.cos(a)))
        rect_y4 = int(image_pos[1] - (rect_width * math.sin(a)) - (rect_height * math.cos(a)))
        vertices = [rect_x1,rect_y1,rect_x2,rect_y2,rect_x3,rect_y3,rect_x4,rect_y4,rect_x1,rect_y1]
        print(vertices)
        return vertices



class DisplayLabel(Label):

    def __init__(self, image_coords=(0,0), image_angle=0,image_size=(200,200), **kwargs):
        self.text = 'testing'
        self.font_size = 30
        self.size_hint = (None,None)
        self.halign = 'center'
        self.valign = 'middle'
        self.size = self.texture_size
        self.angle_u = self.correct_angle(image_angle)
        # self.pos = (image_coords[0], image_coords[1]-(image_size[1]*2))
        self.pos = self.relative_pos(image_coords=image_coords, image_angle=self.angle_u, image_size=image_size)
        
        super(DisplayLabel, self).__init__(**kwargs)

        with self.canvas.before:
            PushMatrix()
            Rotate(angle=self.angle_u, axis=(0,0,1), origin=self.center)
        with self.canvas.after:
            PopMatrix()


    def relative_pos(self,image_coords, image_angle, image_size):

        new_x = image_coords[0] + ((1.5 * image_size[1]) * math.cos(math.radians(image_angle + 90)))
        new_y = image_coords[1] + ((1.5 * image_size[1]) * math.sin(math.radians(image_angle + 90)))
        new_coords = (int(new_x), int(new_y))
        print(new_coords)
        return new_coords


    def correct_angle(self, image_angle):
        if image_angle > 90 and image_angle < 270:
            return image_angle - 180
        elif image_angle > 270 and image_angle < 360:
            return image_angle - 360
        else:
            return image_angle


class CalibrationLine(Button):
    def __init__(self, **kwargs):
        self.text = 'REMOVE CALIBRATION LINE'
        self.font_size = 10
        self.size_hint = (None,None)
        self.size=(150,50)
        self.pos = (0,60)
        
        super(CalibrationLine, self).__init__(**kwargs)
        with self.canvas.after:
            Color(1,0,0,1, mode='rgba')
            Line(points=(120,5,1120,5), width=5)


class NextStepButton(Button):
    def __init__(self, **kwargs):
        self.text = 'NEXT STEP'
        self.font_size = 20
        self.size_hint = (None,None)
        # self.halign = 'center'
        # self.valign = 'middle'
        # self.size = self.texture_size
        self.size=(150,50)
        self.pos = (0,10)
        
        super(NextStepButton, self).__init__(**kwargs)


class MyLayout(FloatLayout):
    #You don't need to understand these 2 lines to make it work!
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        #layout = ScatterLayout()
        self.image_one = DisplayImage()
        self.add_widget(self.image_one)
        self.label_one = DisplayLabel(image_coords=self.image_one.coords, image_angle=self.image_one.angle, image_size=self.image_one.size)
        self.add_widget(self.label_one)
        self.image_two=DisplayImage()
        self.label_two=DisplayLabel(image_coords=self.image_two.coords, image_angle=self.image_two.angle, image_size=self.image_one.size)
        self.add_widget(self.image_two)
        self.add_widget(self.label_two)

        self.next_step = NextStepButton()
        self.next_step.bind(on_press=self.button_pressed)
        self.add_widget(self.next_step)

        self.calibration = CalibrationLine()
        self.calibration.bind(on_press=self.remove_calibration)
        self.add_widget(self.calibration)
        
        self.cvx = Cvx_comms()

        Clock.schedule_interval(self.move_images, 1)

    def button_pressed(self, *args):
        print('button was pressed!')


    def remove_calibration(self, *args):
        self.remove_widget(self.calibration)
        #print('removing button!')

    def move_images(self, image_one):
        try:
            image_one_coords, image_two_coords = self.cvx.coords()
            if len(image_one_coords) == 3:
                self.remove_widget(self.image_one)
                self.remove_widget(self.label_one)
                self.remove_widget(self.image_two)
                self.remove_widget(self.label_two)
                self.image_one = DisplayImage(coords=(image_one_coords[0], image_one_coords[1]), angle=image_one_coords[2])
                self.image_two = DisplayImage(coords=(image_two_coords[0], image_two_coords[1]), angle=image_two_coords[2])
                self.label_one = DisplayLabel(image_coords=self.image_one.coords, image_angle=self.image_one.angle, image_size=self.image_one.size)
                self.label_two = DisplayLabel(image_coords=self.image_two.coords, image_angle=self.image_two.angle, image_size=self.image_two.size)
                self.add_widget(self.image_one)
                self.add_widget(self.label_one)
                self.add_widget(self.image_two)
                self.add_widget(self.label_two)
        except:
            print('Error in move images')



    def test_move(self, dt):
        self.remove_widget(self.image_one)
        self.remove_widget(self.label_one)
        if hasattr(self, 'image_two'):
            self.remove_widget(self.image_two)
            self.remove_widget(self.label_two)
        rw = random.randint(100,500)
        rh = random.randint(100,500)
        ra = random.randint(0,360)
        self.image_one = DisplayImage(coords=(rw,rh), angle=ra)
        self.image_two = DisplayImage(coords=(rh,rw), angle=ra)
        self.label_one = DisplayLabel(image_coords=self.image_one.coords, image_angle=self.image_one.angle, image_size=self.image_one.size)
        self.label_two = DisplayLabel(image_coords=self.image_two.coords, image_angle=self.image_two.angle, image_size=self.image_two.size)
        self.add_widget(self.image_one)
        self.add_widget(self.label_one)
        self.add_widget(self.image_two)
        self.add_widget(self.label_two)


class Calibration():
    #This class will contain all the business logic required to scale everything else
    pass

class Step():
    #this class will contain all the logic to get the stuff out of the csv file
    pass





class Cvx_comms():

    def get_string_from_serial(self):
        #Checks that we have data to read
        #Does not wait for data (to not hang the main loop)
        #print("number of lins in the queue: " + str(serial_device.inWaiting()))
        if not serial_device.inWaiting() > 0:
            #pass
            return None
        else:
            return serial_device.readline().decode()
            # print(received_string)

    def coords(self):
        ### TESTING IF STATEMENT.
        ### ONCE SERIAL PORT IS CONNECTED, REMOVE THIS!!!
        if True:
            im1x = random.randint(100,500)
            im1y = random.randint(100,500)
            im1a = random.randint(0,360)
            im2x = random.randint(100,500)
            im2y = random.randint(100,500)
            im2a = random.randint(0,360)

            return [im1x, im1y, im1a], [im2x, im2y,im2a]

        #checks if there is a waiting string, if there is it parses it out into coords and returns it
        try:
            self.rec_string = self.get_string_from_serial()    
             

            # trash_chars = {'\r': '', '\n': '', '+':'','-':''}
            # for a,b in trash_chars.items():
            #     rec_string = rec_string.replace(a, b)

            trash_chars = ['\r', '\n', '+', '-']
            for char in trash_chars:
                self.rec_string = self.rec_string.replace(char, '')


            self.parts_coords = self.rec_string.split(';')
            print(self.part_coords)
            print("Recevied ", len(self.part_coords), "part coordinaates.")

            for part in self.parts_coords:
                part_one_coords, part_two_coords = part.split(',')
                return part_one_coords, part_two_coords
                #kivy.do_stuff_with_coords(coords[0], coords[1], coords[2])
        except:
            pass


# cvx = Cvx_comms()
# #kivy = Kivy()

# string = '+620,-360,0;-456,-123,+50\r\n'


# cvx.extract_coords(string)

        
class ARDemo(App):
    def build(self):
        Display = MyLayout()
        
        return Display

if __name__ == "__main__":
    
    #Before launching GUI open serial connection
    print("Connecting to serial device.")
    try:
        #NORMAL RS232 CONNECTION:
        # ser = serial.Serial(
        #     port='COM4',
        #     baudrate=115200,
        #     bytesize=serial.EIGHTBITS,
        #     parity=serial.PARITY_EVEN,
        #     stopbits=serial.STOPBITS_ONE,
        # )

        #USB-COM RS232 CONNECTION
        #used for testing with SRG usb

        serial_device = serial.Serial('COM11')
        print("CONNECTION SUCCESSFUL!")

    except:
        print("Failed to connect to serial port!")
        #exit()

    ARDemo().run()
    serial.close()












