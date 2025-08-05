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
from shuffle.move_sequence import MovesDB, MoveSequenceGenerator
from shuffle.path_config import DATADIR


class ManualSlides(Widget):
    element1 = ObjectProperty(None) # defined in text.kv
    element2 = ObjectProperty(None) # defined in text.kv
    element3 = ObjectProperty(None) # defined in text.kv
    element4 = ObjectProperty(None) # defined in text.kv
    gen = ObjectProperty(MoveSequenceGenerator(MovesDB(DATADIR / "moves.csv")))

    def rotate(self, blu):
        self.gen.pointer += 1
        elements = [self.element1, self.element2, self.element3, self.element4]
        for el in elements:
            diff = self.width/2
            if el.x + el.width <= 0:
                el.x = self.width + self.width / 2
            anim = Animation(x=el.x-diff, y=el.y, duration=0.5)
            anim.start(el)
        if self.gen.pointer >= len(self.gen.sequence):
            self.gen.generate_batch()
        elements[self.gen.pointer % len(elements)].text = self.gen.sequence[self.gen.pointer]


class SlidesApp(App):
    def build(self):
        app = ManualSlides()
        app.element1.text = app.gen.walk()
        app.element2.text = app.gen.walk()
        app.element3.text = app.gen.walk()
        app.element4.text = app.gen.walk()
        Clock.schedule_interval(app.rotate, 2 * 70.0 / 50.0)# / 60.0)
        #140 / 70 Bring Ban Bang Born

        return app


if __name__ == '__main__':
    SlidesApp().run()