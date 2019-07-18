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

class TouchMixin(object):

    def __init__(self, *args, **kwargs):
        super(TouchMixin, self).__init__(*args, **kwargs)
        self.register_event_type('touch_down')

    def touch_down(self, touch):
        pass

class CellWidget(Button):

    #Cell size
    cell_size = 35

    def __init__(self, row, col, **kwargs):
        super(CellWidget, self).__init__(**kwargs, size_hint=(None, None), size=(self.cell_size, self.cell_size))
        self.bind(on_press=self.callback)
        self.row = row
        self.col = col

    def callback(self, instance):
        print('(' + str(self.row) + ', ' + str(self.col) + ')')

class MapWidget(GridLayout):

    #Map size
    map_size = 100

    def __init__(self, **kwargs):
        GridLayout.__init__(self, size_hint=(1, 1 - 175 / 805), rows=self.map_size, cols=self.map_size, pos=(0, 3045))
        for row in range(self.map_size):
            for col in range(self.map_size):
                self.add_widget(CellWidget(row, col))

class ZoomWidget(ScatterLayout):

    def __init__(self, **kwargs):
        ScatterLayout.__init__(self, size_hint=(1, 1 - 175 / 805), pos=(0, 175))

    def on_touch_down(self, touch):
        # for child in Widget.children:
        #     if child is self: continue
        #     if child.collide_point(*touch.pos):
        #         return super(ZoomWidget, self).on_touch_down(touch)
        #     else:
        if touch.button == 'scrollup':
            if self.scale <= 1:
                self.scale = self.scale * 0.9
                self.w
        if touch.button == 'scrolldown':
            self.scale = self.scale * 1.03 if self.scale < 1 else 1

class MappingUtilApp(App):

    def build(self):
        #Initializing window size
        Window.size = (805, 805)
        Window.bind(on_resize=self.disable_window_resize)

        #Root widget
        root = FloatLayout()

        #The interactive map
        interactive_map = ZoomWidget()
        interactive_map.add_widget(MapWidget())
        root.add_widget(interactive_map)

        return root

    def disable_window_resize(self, instance, x, y):
        if x != 805 or y != 805:
            Window.size = (805, 805)

if __name__ == '__main__':
    MappingUtilApp().run()