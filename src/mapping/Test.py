from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.behaviors import DragBehavior
from kivy.graphics import Color
from kivy.config import Config
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import *
from Map import Map

#(0, 0) is bottom left of the window

#Disabling border
#Config.set('graphics', 'fullscreen', 'fake')

#Disabling multitouch
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class CellWidget(Button):

    #Cell size
    cell_size = 17

    def __init__(self, row, col, **kwargs):
        super(CellWidget, self).__init__(**kwargs, size_hint=(None, None), size=(self.cell_size, self.cell_size))
        self.bind(on_press=self.callback)
        self.row = row
        self.col = col

    def callback(self, instance):
        print('(' + str(self.row) + ', ' + str(self.col) + ')')

class MapWidget(GridLayout):

    #Map size
    map_size = 50

    def __init__(self, **kwargs):
        GridLayout.__init__(self, rows=self.map_size, cols=self.map_size)
        for row in range(self.map_size):
            for col in range(self.map_size):
                self.add_widget(CellWidget(row, col))

class ZoomWidget(ScatterLayout, Widget):

    def __init__(self, **kwargs):
        ScatterLayout.__init__(self)
        # self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
        # self.keyboard.bind(on_key_down=self.on_keyboard_down)

    # def keyboard_closed(self):
    #     self.keyboard.unbind(on_key_down=self.on_keyboard_down)
    #     self.keyboard = None

    # def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    #     if keycode[1] == 'left':
    #         self.grid_zoom(False)
    #     elif keycode[1] == 'right':
    #         self.grid_zoom(True)

    # def on_touch_down(self, touch):
    #     if touch.button == 'scrollup':
    #         self.scale = self.scale * 1.03 if self.scale <= 1 else 1
    #         self.pos = (0, 175)
    #     elif touch.button == 'scrolldown':
    #         self.scale = self.scale * 0.9 if self.scale >= 0.5 else 0.5
    #         self.pos = (0, 175)                        

    # def grid_zoom(self, zoom_in):
    #     if zoom_in:
    #         self.scale = self.scale * 1.1
    #         self.pos = (0, 0)
    #     else:
    #         self.scale = self.scale * 0.9
    #         self.pos = (0, 0)

class MappingUtilApp(App):

    #Window dimensions
    x = 850
    y = 850

    def build(self):
        #Initializing window
        Window.size = (self.x, self.y)
        Window.bind(on_resize=self.disable_window_resize)

        #Root widget
        root = FloatLayout()

        #The interactive map
        interactive_map = ZoomWidget()
        interactive_map.add_widget(MapWidget())
        root.add_widget(interactive_map)

        return root

    def disable_window_resize(self, instance, x, y):
        if x != self.x or y != self.y:
            Window.size = (self.x, self.y)

if __name__ == '__main__':
    MappingUtilApp().run()