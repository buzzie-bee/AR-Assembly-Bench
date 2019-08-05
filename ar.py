from kivy.config import Config
screen_width = 1013
screen_height = 850
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
import pandas
from PIL import Image as PILImage

class DisplayImage(Image):

    def __init__(self,image_num=1,coords=(620,360), angle=315,filename='keyence.png', object_width = 100, object_height=200, **kwargs):
        image = ImageProps(filename=filename, object_width=object_width, object_height=object_height)
        self.source=filename
        
        #TODO - change the size to be a scaled thing
        self.size= image.size
        self.size_hint=(None,None)
        self.allow_stretch=(True)
        self.coords = coords
        self.pos= (coords[0]-image.offset[0], coords[1] - image.offset[1])
        self.angle = angle
        #print(self.pos)

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
            # turned off since the screen size change
            # Line(points=(620,0,620,720), width=1)
            

class ImageProps():

    def __init__(self, filename='keyence.png', object_width=100, object_height=100):

        #print("looking up image props")
        with PILImage.open(filename) as image:
            width, height = image.size

        self.size = scale.scale_image(width, height, object_width, object_height)
        #self.size = (width,height)
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
        #print(vertices)
        return vertices



class DisplayLabel(Label):

    def __init__(self, image_coords=(0,0), image_angle=0,image_size=(200,200), label_text='', **kwargs):
        self.text = label_text
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
        #print(new_coords)
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
            Line(points=(7,5,1007,5), width=5)


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
        self.cvx = Cvx_comms()
        self.step = Step()


        self.image_one = DisplayImage()
        self.add_widget(self.image_one)
        self.label_one_text = ''
        self.label_two_text=''
        self.label_one = DisplayLabel(image_coords=self.image_one.coords, image_angle=self.image_one.angle, image_size=self.image_one.size)
        self.image_two=DisplayImage(image_num='test')
        #self.image_two=DisplayImage()
        self.label_two=DisplayLabel(image_coords=self.image_two.coords, image_angle=self.image_two.angle, image_size=self.image_one.size)
        self.add_widget(self.image_two)
        self.add_widget(self.label_two)

        self.next_step_button = NextStepButton()
        self.next_step_button.bind(on_press=self.next_step)
        self.add_widget(self.next_step_button)

        self.calibration = CalibrationLine()
        self.calibration.bind(on_press=self.remove_calibration)
        self.add_widget(self.calibration)
        
        
        Clock.schedule_interval(self.move_images, 1)
        #Clock.schedule_interval(self.test_move_images, 1)

    def button_pressed(self, *args):
        print('button was pressed!')


    def next_step(self, *args):
        if self.step.step_count < self.step.max_step:
            self.step.increment()
        else:
            self.step.reset()

    def remove_calibration(self, *args):
        self.remove_widget(self.calibration)
        #print('removing button!')

    def move_images(self, image_one):

        try:
            raw_image_one_coords, raw_image_two_coords = self.cvx.coords()
            image_one_coords = scale.scale_coordinates(raw_image_one_coords[0],raw_image_one_coords[1],raw_image_one_coords[2])
            image_two_coords = scale.scale_coordinates(raw_image_two_coords[0],raw_image_two_coords[1],raw_image_two_coords[2])

            image_one_filename, object_one_width, object_one_height, label_one_text, image_two_filename, object_two_width, object_two_height, label_two_text = self.step.get_step_properties()
            print(image_one_filename, object_one_width, object_one_height, label_one_text, image_two_filename, object_two_width, object_two_height, label_two_text)
            if len(image_one_coords) == 3:
                self.remove_widget(self.image_one)
                self.remove_widget(self.label_one)
                self.remove_widget(self.image_two)
                self.remove_widget(self.label_two)
                self.image_one = DisplayImage(coords=(image_one_coords[0], image_one_coords[1]), angle=image_one_coords[2], filename=image_one_filename, object_width=object_one_width, object_height=object_one_height)
                self.image_two = DisplayImage(coords=(image_two_coords[0], image_two_coords[1]), angle=image_two_coords[2], filename=image_two_filename, object_width=object_two_width, object_height=object_two_height)
                self.label_one = DisplayLabel(image_coords=self.image_one.coords, image_angle=self.image_one.angle, image_size=self.image_one.size, label_text=label_one_text)
                self.label_two = DisplayLabel(image_coords=self.image_two.coords, image_angle=self.image_two.angle, image_size=self.image_two.size, label_text=label_two_text)
                self.add_widget(self.image_one)
                self.add_widget(self.label_one)
                self.add_widget(self.image_two)
                self.add_widget(self.label_two)
        except:
            print('Error in move images')


class Step():
    #this class will contain all the logic to get the stuff out of the csv file
    def __init__(self, *args):
        self.step_count = 0
        self.max_step=10
        self.filenames = 'keyence.png', 'keyence.png'
        self.labels = '',''

    def max_step(self):
        return self.max_step

    def set_max_step(self, max_steps=10):
        self.max_step = max_steps

    def get_step_properties(self):
        steps_list = pandas.read_csv('steps.csv', index_col='step_number')
        
        self.set_max_step(steps_list.shape[0] - 1)
        print("max step count is: ", self.max_step)

        step_dict = steps_list.loc[int(self.step_count)]

        image_one_filename = step_dict['image_one_filename']
        object_one_width = int(step_dict['image_one_width'])
        object_one_height = int(step_dict['image_one_height'])
        label_one_text = step_dict['image_one_label_text']

        image_two_filename = step_dict['image_two_filename']
        object_two_width = int(step_dict['image_one_width'])
        object_two_height = int(step_dict['image_one_height'])
        label_two_text = step_dict['image_two_label_text']

        return image_one_filename, object_one_width, object_one_height, label_one_text, image_two_filename, object_two_width, object_two_height, label_two_text

    def increment(self, *args):
        self.step_count += 1

    def reset(self, new_starting_step=0):
        self.step_count = new_starting_step



class Scaling():
    #This class will contain all the business logic required to scale everything else
    def __init__(self, **kwargs):
        #FOR NOW
        #CHANGE THIS VALUE AFTER MEASURING SCREEN AND RESTART PROGRAM
        measured_line_width_mm=1150

        scale_line_width_pixels = 1000
        self.pixels_per_mm = measured_line_width_mm / scale_line_width_pixels


        camera_width=2432
        camera_height=2040
        self.scaled_ratio_x = camera_width / screen_width
        self.scaled_ratio_y = camera_height / screen_height

        # screen_width = 1013
        # screen_height = 850
        #camera field of view in pixels:
        # width = 2432
        # height = 2040

        camera_width=2432
        camera_height=2040
        
    def scale_coordinates(self, camera_x, camera_y, angle):
        #get the x,y coords from the camera and scale them to accurately portray them on the screen

        
        scaled_x = camera_x / self.scaled_ratio_x
        scaled_y = camera_y / self.scaled_ratio_y

        # #Potentially needed feature! Offset camera x,y by some pixels to account for difference in mounting position of camera
        # offset_x = -100
        # offset_y = +50

        # scaled_x += offset_x
        # scaled_y += offset_y

        return int(scaled_x), int(scaled_y), angle

    def scale_image(self, image_width, image_height, object_width, object_height):
        px_to_width_ratio = image_width / object_width
        px_to_height_ratio = image_height / object_height
        screen_width_ratio = self.pixels_per_mm / px_to_width_ratio
        screen_height_ratio = self.pixels_per_mm / px_to_width_ratio
        scaled_width = screen_width_ratio * image_width
        scaled_height = screen_height_ratio * image_height

        return int(scaled_width), int(scaled_height)

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


        camera_width=2432
        camera_height=2040

        if True:
            im1x = random.randint(100,2432)
            im1y = random.randint(100,2040)
            im1a = random.randint(0,360)
            im2x = random.randint(100,2432)
            im2y = random.randint(100,2040)
            im2a = random.randint(0,360)

            return [im1x, im1y, im1a], [im2x, im2y,im2a]

        #checks if there is a waiting string, if there is it parses it out into coords and returns it
        try:
            self.rec_string = self.get_string_from_serial()    

            trash_chars = ['\r', '\n', '+', '-']
            for char in trash_chars:
                self.rec_string = self.rec_string.replace(char, '')


            self.parts_coords = self.rec_string.split(';')

            for part in self.parts_coords:
                part_one_coords, part_two_coords = part.split(',')
                return part_one_coords, part_two_coords
        except:
            pass

        
class ARDemo(App):
    def build(self):
        Display = MyLayout()
        
        return Display

if __name__ == "__main__":

    scale = Scaling()
    # print("scaled x,y = ", scale.scale_coordinates(1,2,3))
    
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












