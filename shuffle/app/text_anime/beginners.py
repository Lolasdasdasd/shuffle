import random
import time
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty, ListProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.animation import Animation
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty, ListProperty
)

from shuffle.app.text_anime.slides import ManualSlides

class Counter(Button):

    counter = NumericProperty(0)
    counter_string = StringProperty("Click to count")
    

    def add(self):
        self.counter += 1
        self.counter_string = f"Counter: {self.counter}"
        

class BPMDetector(Counter):
    times = ListProperty()
    local_bpm = NumericProperty(0)
    global_bpm = NumericProperty(0)
    frame_size = NumericProperty(0) # number of beats that define bpm

    def __init__(self, **kwargs):#frame_size=3):
        super(BPMDetector, self).__init__(**kwargs)
        if "frame_size" in kwargs:
            self.frame_size = kwargs["frame_size"]
        else:
            self.frame_size = 5
        self.counter_string = "BPM Detector"

    def add(self):
        super().add()
        self.calc_bpm()
    
    def calc_bpm(self):
        current_time = time.time()
        self.times.append(current_time)
        if len(self.times) >= self.frame_size:
            beats = len(self.times) - 1
            time_min = (current_time - self.times[0]) / 60.0
            self.global_bpm = beats / time_min

            trim = self.times[(len(self.times)-self.frame_size):]
            beats = len(trim) - 1 # should be length of self.frame_size
            time_min = (current_time - trim[0]) / 60.0
            self.local_bpm = beats / time_min

            self.counter_string = f"global bpm: {round(self.global_bpm,0)}\n local bpm: {round(self.local_bpm,0)}"


class Feedback(BoxLayout):

    def __init__(self, **kwargs):
        super(Feedback, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = 100

    def add(self):
        self.counter += 1
        self.counter_string = f"Counter: {self.counter}"
        print("add")
        


class BeginnersApp(App):
    def build(self):
        app = BoxLayout(orientation="vertical")
        #app = GridLayout(cols=1)
        # Feedback
        feedback = Feedback()
        app.add_widget(feedback)

        # Shuffle Move Slides
        slides = ManualSlides()
        Clock.schedule_interval(slides.rotate, 2 * 70.0 / 50.0)# / 60.0)
        app.add_widget(slides)
        args = {"frame_size":3}
        app = BPMDetector(**args)
        return app


if __name__ == '__main__':
    BeginnersApp().run()