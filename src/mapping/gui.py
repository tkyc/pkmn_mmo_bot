from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.actionbar import ActionBar, ActionItem, ActionButton, ActionGroup, ActionView, ActionPrevious, ActionDropDown
from kivy.uix.button import Button
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import *
from Map import Map
from Cell import Cell
from CellType import CellType

###########################
##        Globals        ##
###########################

#Disabling border
#Config.set('graphics', 'fullscreen', 'fake')S

#Disabling multitouch
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

#Actionbar height
actionbar_height = 50

#Window dimensions
window_x = 850
window_y = 900



class CellWidget(Button, Cell):

    #Cell size
    cell_size = NumericProperty(17)

    #Grass cell colour
    grass = ListProperty((124 / 255, 252 / 255, 0, 1))

    #Path cell colour
    path = ListProperty((1, 215 / 255, 0, 1))

    #Target cell colour
    target = ListProperty((1, 0, 0, 1))

    #Prop cell colour
    prop = ListProperty((0.3, 0.3, 0.3, 1))



    def __init__(self, row, col, **kwargs):
        """Constructor.

        Args:
            row - Row index of cell.
            col - Column index of cell.

        Return:
            NONE
        """
        super(CellWidget, self).__init__(size_hint=(None, None), size=(self.cell_size, self.cell_size), row=row, col=col)
        self.bind(on_press=self.set_cell)
        self.enabled_colour = None



    def set_cell(self, instance):
        """Callback for enabling the cell colour and sets the cell type if the cell is clicked.

        Args:
            NONE

        Return:
            NONE
        """
        if self.enabled_colour == CellType.GRASS:
            self.background_color = self.grass
            self.cell_type = CellType.GRASS
        elif self.enabled_colour == CellType.PROP:
            self.background_color = self.prop
            self.cell_type = CellType.PROP
        elif self.enabled_colour == CellType.TARGET:
            self.background_color = self.target
            self.cell_type = CellType.TARGET
        elif self.enabled_colour == CellType.PATH:
            self.background_color = self.path
            self.cell_type = CellType.PATH



    def print_cell_coordinates(self, instance):
        """Prints the cell's row and column indexes.
        
        Args:
            NONE

        Return:
            NONE
        """
        print('(' + str(self.row) + ', ' + str(self.col) + ')')



class MapWidget(GridLayout):

    #Map size
    map_size = NumericProperty(50)



    def __init__(self, **kwargs):
        """Constructor.

        Args:
            NONE

        Return:
            NONE
        """
        super(MapWidget, self).__init__(rows=self.map_size, cols=self.map_size, pos_hint={'top': 1 - actionbar_height / window_y})
        for row in range(self.map_size):
            for col in range(self.map_size):
                self.add_widget(CellWidget(row, col))



    def enable_cell_colour(self, colour):
        """Enables the selected colour for marking on the map/grid.

        Args:
            colour - A CellType. It is one of the following: CellType.GRASS, CellType.PROP, CellType.TARGET, CellType.PATH.

        Return:
            NONE
        """
        for child in self.children:
            child.enabled_colour = colour



class ZoomWidget(ScatterLayout, Widget):

    def __init__(self, **kwargs):
        """Constructor.

        Args:
            NONE

        Return:
            NONE
        """
        super(ZoomWidget, self).__init__()
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)



    def keyboard_closed(self):
        """Unbinds pressed key.

        Args:
            NONE

        Return:
            NONE
        """
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)
        self.keyboard = None



    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        """Callback that handles the key that is pressed.

        Args:
            keyboard - The keyboard.
            keycode - The key being pressed.
            text - N/A
            modifiers - N/A
        
        Return:
            NONE
        """
        if keycode[1] == 'left':
            self.grid_zoom(False)
        elif keycode[1] == 'right':
            self.grid_zoom(True)



    def on_touch_down(self, touch):
        """Handles events withing the app. Overrides Widget class' on_touch_down.

        Args:
            NONE
        
        Return:
            NONE
        """
        if touch.button == 'scrollup':
            self.scale = self.scale * 1.03 if self.scale <= 1 else 1
            self.pos = (0, 175)
        elif touch.button == 'scrolldown':
            self.scale = self.scale * 0.9 if self.scale >= 0.5 else 0.5
            self.pos = (0, 175)                        



    def grid_zoom(self, zoom_in):
        """Performs magnification of the map/grid.

        Args:
            zoom_in - A boolean that determines whether to zoom in or zoom out.

        Return:
            NONE
        """
        if zoom_in:
            self.scale = self.scale * 1.1
            self.pos = (0, 0)
        else:
            self.scale = self.scale * 0.9
            self.pos = (0, 0)



class MappingUtilApp(App):

    def build(self):
        """Renders the app.

        Args:
            NONE

        Return
            NONE
        """
        #Initializing window
        Window.size = (window_x, window_y)
        Window._set_window_pos(Window._get_window_pos()[0], Window._get_window_pos()[1] - 150)
        Window.bind(on_resize=self.disable_window_resize)

        #Root widget
        root = FloatLayout()

        #The interactive map
        interactive_map = MapWidget()
        root.add_widget(interactive_map)
        self.map_gui = interactive_map

        #Action bar
        root.add_widget(self.create_actionbar())

        return root



    def create_actionbar(self):
        """Creates the actionbar.

        Args:
            NONE

        Return:
            NONE
        """
        #Actionbar initialization
        actionbar = ActionBar(pos_hint={'top': 1})
        action_view = ActionView()

        #Spinner initialization
        spinner = ActionGroup(mode='spinner', text='Select')
        grass = ActionButton(text='Grass cell', on_press=self.select_grass)
        prop = ActionButton(text='Prop cell', on_press=self.select_prop)
        target = ActionButton(text='Target cell', on_press=self.select_target)
        path = ActionButton(text='Path cell', on_press=self.select_path)
        spinner.add_widget(grass)
        spinner.add_widget(prop)
        spinner.add_widget(target)
        spinner.add_widget(path)

        #Actionbar buttons
        open = ActionButton(text='Open')
        save = ActionButton(text='Save')
        clear = ActionButton(text='Clear')

        #Add widgets to actionbar
        action_view.add_widget(open)
        action_view.add_widget(save)
        action_view.add_widget(clear)
        action_view.add_widget(spinner)
        action_view.add_widget(ActionPrevious(with_previous=False))
        actionbar.add_widget(action_view)

        return actionbar



    def disable_window_resize(self, instance, x, y):
        """Disables window resizing.

        Args:
            x - The window's current width.
            y - The window's current height.
        """
        if x != window_x or y != window_y:
            Window.size = (window_x, window_y)



    def select_grass(self, instance):
        """Callback for enabling selection of grass on the map/grid.

        Args:
            NONE

        Return:
            NONE
        """
        self.map_gui.enable_cell_colour(CellType.GRASS)



    def select_prop(self, instance):
        """Callback for enabling selection of prop on the map/grid.

        Args:
            NONE

        Return:
            NONE
        """
        self.map_gui.enable_cell_colour(CellType.PROP)



    def select_target(self, instance):
        """Callback for enabling selection of target on the map/grid.

        Args:
            NONE

        Return:
            NONE
        """
        self.map_gui.enable_cell_colour(CellType.TARGET)



    def select_path(self, instance):
        """Callback for enabling selection of path on the map/grid.

        Args:
            NONE

        Return
            NONE
        """
        self.map_gui.enable_cell_colour(CellType.PATH)


#MAIN
if __name__ == '__main__':
    MappingUtilApp().run()