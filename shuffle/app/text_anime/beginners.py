import random
import time
import pandas as pd
from pathlib import Path
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty, ListProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
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

    def reset(self):
        self.times = []
        self.local_bpm = 0
        self.global_bpm = 0
        self.counter = 0
        self.counter_string = "Resetted."

class LabledTextInput(BoxLayout):

    label = ObjectProperty(None)
    input = ObjectProperty(None)

    def __init__(self, label, input, **kwargs):
        super().__init__(**kwargs)
        self.label.text = label
        self.input.text =input


class BPMRegister(BoxLayout):
    def __init__(self, db_path:Path, **kwargs):
        super().__init__(**kwargs)
        self.db_path = db_path
        self.orientation = "vertical"
        if db_path.is_file():
            df = pd.read_csv(db_path.as_posix())
        else:
            df = pd.DataFrame({"interpret":[], "song":[], "bpm":[]})
        self.reg = Register(df, ["interpret", "song"], "bpm")
        self.add_widget(self.reg)
        self.bpm = BPMDetector()
        self.add_widget(self.bpm)

        self.button = Button(text="Reset BPM.")
        self.button.size_hint_y= None
        self.button.height= 100
        self.button.bind(on_press=self.reset_bpm)
        self.add_widget(self.button)

    def reset_bpm(self, instance): # button func
        self.bpm.reset()
        
    def registered(self):
        print("calling registered")
        self.bpm.reset()
        self.write2file()

    def write2file(self):
        self.reg.df.to_csv(self.db_path, index=None)
        print("written")

class Register(BoxLayout):

    def __init__(self,df:pd.DataFrame, keys:list[str], prop:str, **kwargs):
        super().__init__(**kwargs)
        self.df = df
        self.keys = keys
        self.prop = prop

        self.query = RegisterQuery(keys, prop)
        self.add_widget(self.query)
        self.button = Button(text="Submit.")
        self.button.size_hint_y= None
        self.button.height= 100
        self.button.bind(on_press=self.register)
        self.add_widget(self.button)

    def check_existance(self, check_prop:bool=False) -> pd.Index:
        fil = self.df.copy()
        key_values, property_value = self.extract_query_values()
        for i in range(len(key_values)):
            fil = fil.loc[fil[self.keys[i]] == key_values[i]]
        if check_prop:
            fil = fil.loc[fil[self.prop] == property_value]
        return fil.index
    
    def extract_query_values(self):
        key_values = [labledinput.input.text for labledinput in self.query.inputs]
        property_value = key_values.pop()
        return key_values, property_value

    def register(self, instance):
        key_values, property_value = self.extract_query_values()
        N = self.check_existance()#, property_value)
        print(f"N={N} existing entries for key_values")
        #
        d = {self.keys[i]:[key_values[i]] for i in range(len(key_values))}
        new_val = pd.DataFrame(d)
        new_val[self.prop] = property_value
        self.df = pd.concat([self.df, new_val], ignore_index=True, axis=0)
        self.df.set_axis(self.df.columns, axis="columns")
        self.query.clear()
        self.parent.registered()

class RegisterQuery(BoxLayout):
    def __init__(self,keys, prop,**kwargs):
        super().__init__(**kwargs)
        self.keys = keys
        self.property = prop
        self.inputs = []
        for i in range(len(self.keys)):
            w = LabledTextInput(label=self.keys[i], input="Enter value.")
            self.inputs.append(w)
            self.add_widget(w)
        w = LabledTextInput(label=self.property, input="Property to register.")
        self.inputs.append(w)
        self.add_widget(w)

    def clear(self):
        for i in range(len(self.inputs)):
            self.inputs[i].input.text = "" # other field is label

    
    
    


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
        ### READ beginners.kv !! (based on string before "App")
        app = BoxLayout(orientation="vertical")
        #app = GridLayout(cols=1)
        # Feedback
        feedback = Feedback()
        app.add_widget(feedback)

        # Shuffle Move Slides
        slides = ManualSlides()
        Clock.schedule_interval(slides.rotate, 2 * 70.0 / 50.0)# / 60.0)
        app.add_widget(slides)

        #args = {"frame_size":3}
        #app = BPMDetector(**args)
        df = pd.DataFrame({"interpret":[], "song":[], "bpm":[]})
        #args = {"df":df, "keys":["interpret", "song"], "property":"bpm"}
        #app = RegisterQuery(args=args)
        app = Register(df, ["interpret", "song"], "bpm")
        #app = LabledTextInput("Label", "test")

        app = BPMRegister(Path(r"C:\Users\laura\Coding\shuffle\data\bpm.csv"))
        return app


if __name__ == '__main__':
    BeginnersApp().run()