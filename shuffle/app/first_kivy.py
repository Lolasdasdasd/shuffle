import kivy
kivy.require('2.3.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.uix.widget import Widget

def test():
    lab = Label(text='Hello world')
    # TODO place elsewhere
    anim = Animation(x=100, y=100)
    anim.start(lab)
    return lab


class MyApp(App):

    def build(self):
        return test()


if __name__ == '__main__':
    print("run kivy")
    MyApp().run()
    