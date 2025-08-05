import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.label import Label
from shuffle.move_sequence import MovesDB, MoveSequenceGenerator
from shuffle.path_config import DATADIR
moves = ["RM", "Skip", "Brush", "Ski", "RMb"]

# single move
# set of moves
# sequence of moves

class Text(Widget):
    lab = ObjectProperty(None)
    #return lab

    def update(self, df):
        current = self.lab.text
        next = random.choice(moves)
        while current == next:
            next = random.choice(moves)
        self.lab.text=next


class TextSequence(Widget):
    lab = ObjectProperty(None) # defined in text.kv
    lab2 = ObjectProperty(None) # defined in text.kv
    mdb = ObjectProperty(MovesDB(DATADIR / "moves.csv"))
    gen = ObjectProperty(MoveSequenceGenerator(MovesDB(DATADIR / "moves.csv")))

    def update(self, blu):
        m = self.gen.walk()
        self.lab.text=self.lab2.text
        self.lab2.text=m




class TextApp(App):
    def build(self):
        SEQ = 2
        app = TextSequence()
        for i in range(SEQ):
            app.update(3)
        Clock.schedule_interval(app.update, 10.0)# / 60.0)

        return app


if __name__ == '__main__':
    TextApp().run()