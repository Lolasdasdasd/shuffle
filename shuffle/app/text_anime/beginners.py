import random
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
from kivy.uix.anchorlayout import AnchorLayout
from kivy.animation import Animation

from shuffle.app.text_anime.slides import ManualSlides


class Feedback(BoxLayout):

    def __init__(self, **kwargs):
        super(Feedback, self).__init__(**kwargs)
        self.orientation = "horizontal"
        btn1 = Button(text="Hello")
        btn2 = Button(text="World")
        self.add_widget(btn1)
        self.add_widget(btn2)
        self.add_widget(Button(text="!!!"))


class BeginnersApp(App):
    def build(self):
        app = BoxLayout(orientation="vertical")
        # Feedback
        feedback = Feedback()
        app.add_widget(feedback)

        # Shuffle Move Slides
        slides = ManualSlides()
        Clock.schedule_interval(slides.rotate, 2 * 70.0 / 50.0)# / 60.0)
        app.add_widget(slides)
        
        



        #BeginnersWrapper()

        return app


if __name__ == '__main__':
    BeginnersApp().run()