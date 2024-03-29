import os
import pickle
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.actionbar import ActionBar, ActionItem, ActionButton, ActionGroup, ActionView, ActionPrevious, ActionDropDown
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.spinner import Spinner
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import *
from mapping.Cell import Cell
from mapping.CellType import CellType
from mapping.Map import Map
from src.scripts.wild_training import execute_training

###########################
##        Globals        ##
###########################

#Disabling multitouch
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

#Actionbar height
actionbar_height = 50

#Window dimensions
window_x = 850
window_y = 900

#Map size (50 x 50)
map_size = 50

#Cell size
cell_size = 17



class CellWidget(Button, Cell):

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
        super(CellWidget, self).__init__(size_hint=(None, None), size=(cell_size, cell_size), row=row, col=col)
        
        #Default cell type/colour selection
        self.enable_colour_of_type = CellType.PATH



    def set_cell(self, instance=None):
        """Sets the cell colour and type depending on the enabled_colour_of_type instance variable.

        Args:
            instance - N/A

        Returns:
            NONE
        """
        #Grass cell
        if self.enable_colour_of_type == CellType.GRASS:
            self.background_color = self.grass
            self.cell_type = CellType.GRASS

        #Prop cell
        elif self.enable_colour_of_type == CellType.PROP:
            self.background_color = self.prop
            self.cell_type = CellType.PROP

        #Target cell
        elif self.enable_colour_of_type == CellType.TARGET:
            self.background_color = self.target
            self.cell_type = CellType.TARGET

        #Path cell
        elif self.enable_colour_of_type == CellType.PATH:
            self.background_color = self.path
            self.cell_type = CellType.PATH

        #Null cell
        elif self.enable_colour_of_type == None:
            self.background_color = (1, 1, 1, 1)



    def on_touch(self, touch):
        """Handles mouse events.

        Args:
            touch - The mouse event.
        
        Return:
            NONE
        """
        if self.collide_point(*touch.pos):
            if touch.button == 'right':
                self.background_color = (1, 1, 1, 1)
                self.cell_type = None
            if touch.button == 'left':
                self.set_cell()
            return True



    def on_touch_down(self, touch):
        """Assigns/unassigns cell type by mouse click.

        Args:
            touch - The touch event.

        Returns:
            NONE
        """
        self.on_touch(touch)



    def on_touch_move(self, touch):
        """Assigns/unassigns cell type by mouse drag.

        Args:
            touch - The touch event.

        Returns:
            NONE
        """
        self.on_touch(touch)



    def print_cell_coordinates(self):
        """Prints the cell's row and column indexes.
        
        Args:
            NONE

        Returns:
            NONE
        """
        print('(' + str(self.row) + ', ' + str(self.col) + ')')



class MapWidget(GridLayout):

    def __init__(self, **kwargs):
        """Constructor.

        Args:
            NONE

        Return:
            NONE
        """
        super(MapWidget, self).__init__(rows=map_size, cols=map_size, pos_hint={'top': 1 - actionbar_height / window_y})
        for row in range(map_size):
            for col in range(map_size):
                self.add_widget(CellWidget(row, col))

        #Saved/opened map from file
        self.map = None



    def enable_cell_colour(self, cell_type):
        """Enables the selected colour for marking on the map/grid.

        Args:
            cell_type - A CellType. It is one of the following: CellType.GRASS, CellType.PROP, CellType.TARGET, CellType.PATH.

        Returns:
            NONE
        """
        for child in self.children:
            child.enable_colour_of_type = cell_type



    def clear_map(self, instance=None):
        """Clears the map and resets cell type.

        Args:
            NONE

        Returns:
            NONE
        """
        self.map = None
        for child in self.children:
            child.background_color = (1, 1, 1, 1)
            child.cell_type = None



class ActionBarWidget(ActionBar):
    """The ActionBarWidget is used to move the program window.
    """


    def __init__(self, app, **kwargs):
        """Constructor. Initialize the actionbar last after all other widgets.
           This widget depends on some functions from other widgets.

        Args:
            app - The application.

        Returns:
            NONE
        """
        #Actionbar initialization
        super(ActionBarWidget, self).__init__(pos_hint={'top': 1})
        action_view = ActionView()
        action_prev = ActionPrevious(with_previous=False, app_icon='icon.png', app_icon_height=actionbar_height / 2, app_icon_width=actionbar_height / 2)
        #Used to calculate direction vector to move window
        self.mouse_x = None
        self.mouse_y = None

        #Spinner initialization
        spinner = ActionGroup(mode='spinner', text='Select')
        grass = ActionButton(text='Grass cell', on_press=lambda instance : app.map_gui.enable_cell_colour(CellType.GRASS))
        prop = ActionButton(text='Prop cell', on_press=lambda instance : app.map_gui.enable_cell_colour(CellType.PROP))
        target = ActionButton(text='Target cell', on_press=lambda instance : app.map_gui.enable_cell_colour(CellType.TARGET))
        path = ActionButton(text='Path cell', on_press=lambda instance : app.map_gui.enable_cell_colour(CellType.PATH))
        spinner.add_widget(grass)
        spinner.add_widget(prop)
        spinner.add_widget(target)
        spinner.add_widget(path)

        #Actionbar buttons
        Run = ActionButton(text='Run', on_press=lambda instance : app.run_menu_popup.open())
        open = ActionButton(text='Open', on_press=lambda instance : app.file_chooser_popup.open())
        save = ActionButton(text='Save', on_press=app.serialize_map)
        clear = ActionButton(text='Clear', on_press=app.map_gui.clear_map)

        #Add widgets to actionbar
        action_view.add_widget(Run)
        action_view.add_widget(open)
        action_view.add_widget(save)
        action_view.add_widget(clear)
        action_view.add_widget(spinner)
        action_view.add_widget(action_prev)
        self.add_widget(action_view)



    def on_touch_down(self, touch):
        """Get the current mouse position on right click.

        Args:
            touch - The mouse event.

        Returns:
            boolean - True if collision with action bar, otherwise propagate mouse event.
        """
        if self.collide_point(*touch.pos):
            if touch.button == 'right':
                self.mouse_x = touch.pos[0]
                self.mouse_y = touch.pos[1]
                return True
        return super(ActionBarWidget, self).on_touch_down(touch)



    def on_touch_move(self, touch):
        """Get the mouse position as the mouse is dragged.

        Args:
            touch - The mouse event.

        Returns:
            boolean - True if collision with action bar, otherwise propagate mouse event.
        """
        if self.collide_point(*touch.pos):
            if touch.button == 'right':
                # direction = math.atan2(touch.pos[1] - self.mouse_y, touch.pos[0] - self.mouse_x)
                # x_direction = round(math.cos(direction))
                # y_direction = round(math.sin(direction))
                # Window.top = Window.top - (y_direction * 2)
                # Window.left = Window.left + (x_direction * 2)
                # self.mouse_x = touch.pos[0]
                # self.mouse_y = touch.pos[1]
                x_direction = touch.pos[0] - self.mouse_x
                y_direction = touch.pos[1] - self.mouse_y
                Window.top = Window.top - y_direction
                Window.left = Window.left + x_direction
                return True
        return super(ActionBarWidget, self).on_touch_down(touch)



class ZoomWidget(ScatterLayout, Widget):

    def __init__(self, **kwargs):
        """Constructor.

        Args:
            NONE

        Returns:
            NONE
        """
        super(ZoomWidget, self).__init__()
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)



    def keyboard_closed(self):
        """Unbinds pressed key.

        Args:
            NONE

        Returns:
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
        
        Returns:
            NONE
        """
        if keycode[1] == 'left':
            self.grid_zoom(False)
        elif keycode[1] == 'right':
            self.grid_zoom(True)



    # def on_touch_down(self, touch):
    #     """Handles instances withing the app. Overrides Widget class' on_touch_down.

    #     Args:
    #         NONE
        
    #     Returns:
    #         NONE
    #     """
    #     if touch.button == 'scrollup':
    #         self.scale = self.scale * 1.03 if self.scale <= 1 else 1
    #         self.pos = (0, 175)
    #     elif touch.button == 'scrolldown':
    #         self.scale = self.scale * 0.9 if self.scale >= 0.5 else 0.5
    #         self.pos = (0, 175)                        



    # def grid_zoom(self, zoom_in):
    #     """Performs magnification of the map/grid.

    #     Args:
    #         zoom_in - A boolean that determines whether to zoom in or zoom out.

    #     Returns:
    #         NONE
    #     """
    #     if zoom_in:
    #         self.scale = self.scale * 1.1
    #         self.pos = (0, 0)
    #     else:
    #         self.scale = self.scale * 0.9
    #         self.pos = (0, 0)



class MappingUtilApp(App):

    def build(self):
        """Renders the app.

        Args:
            NONE

        Returns:
            NONE
        """
        #Initializing window
        Window.size = (window_x, window_y)
        Window._set_window_pos(Window._get_window_pos()[0], Window._get_window_pos()[1] - 150)
        Window.bind(on_resize=self.disable_window_resize)
        Window.borderless = True
        self.icon = 'icon.png'

        #Root widget
        root = FloatLayout()

        #Child widgets
        map = MapWidget()
        self.map_gui = map

        serialization_success_popup = self.create_serialization_success_popup()
        self.serialization_success_popup = serialization_success_popup

        file_chooser_popup = self.create_file_chooser()
        self.file_chooser_popup = file_chooser_popup

        run_menu_popup = self.create_run_menu()
        self.run_menu_popup = run_menu_popup

        actionbar = ActionBarWidget(self)
        self.actionbar = actionbar

        root.add_widget(map)
        root.add_widget(actionbar)

        return root



    def create_run_menu(self):
        """Creates the run menu popup.

        Args:
            NONE

        Returns:
            NONE
        """
        #Initializing widgets
        run_menu_popup = Popup(size_hint=(0.7, 0.4), auto_dismiss=True, separator_height=0, title='')

        scripts = os.listdir('../scripts/')
        del scripts[-1]
        spinner = Spinner(text='Select', values=scripts, size_hint=(1, 0.008), pos_hint={'top': 1})

        run_button = Button(text='Run script', on_press=lambda instance : self.run_script(spinner.text))
        cancel_button = Button(text='Stop script', on_press=run_menu_popup.dismiss)

        #Organizing layout
        box_layout = BoxLayout(orientation='vertical')
        grid_layout = GridLayout(rows=1, cols=2, size_hint=(1, 0.07), padding=(10, 250, 10, 5), spacing=(10, 0))
        box_layout.add_widget(spinner)
        grid_layout.add_widget(run_button)
        grid_layout.add_widget(cancel_button)
        box_layout.add_widget(grid_layout)
        run_menu_popup.add_widget(box_layout)
        
        return run_menu_popup



    def run_script(self, script):
        """Run the selected script.

        Args:
            script - The name of the script.

        Returns:
            NONE
        """
        self.run_menu_popup.dismiss()
        execute_training(self.map_gui.map)



    def create_file_chooser(self):
        """Creates the file chooser popup.

        Args:
            NONE

        Returns:
            NONE
        """
        #Initializing widgets
        file_chooser_popup = Popup(size_hint=(0.7, 0.8), auto_dismiss=True, separator_height=0, title='')
        file_chooser = FileChooserListView()
        load_button = Button(text='Load', on_press=lambda instance : self.open_serialized_map(file_chooser.path, file_chooser.selection))
        cancel_button = Button(text='Cancel', on_press=file_chooser_popup.dismiss)

        #Organizing layout
        box_layout = BoxLayout(orientation='vertical')
        grid_layout = GridLayout(rows=1, cols=2, size_hint=(1, 0.07), padding=(10, 10, 10, 5), spacing=(10, 0))
        box_layout.add_widget(file_chooser)
        grid_layout.add_widget(load_button)
        grid_layout.add_widget(cancel_button)
        box_layout.add_widget(grid_layout)
        file_chooser_popup.add_widget(box_layout)

        return file_chooser_popup



    def serialize_map(self, instance=None):
        """Save the map/grid.

        Args:
            instance - N/A

        Returns:
            NONE
        """
        #Serialize map (serializing widgets is not possible)
        serial_map = Map(map_size, map_size)
        self.map_gui.map = serial_map
        for child in self.map_gui.children:
            serial_cell = Cell(child.row, child.col)
            serial_cell.cell_type = child.cell_type
            serial_map.matrix[child.row][child.col] = serial_cell

        with open('serialized_map.config', 'wb') as serialized_map_config:
            pickle.dump(serial_map, serialized_map_config)

        #Serialization success popup
        self.serialization_success_popup.open()



    def open_serialized_map(self, path, filename):
        """Load the serialized map into the app.

        Args:
            path - The path to the directory.
            filename - The name of serialized map file.

        Returns:
            NONE
        """
        try:
            path = os.path.join(path, filename[0])
            with open(path, 'rb') as serialized_map:
                map = pickle.load(serialized_map)
                self.map_gui.map = map
                for child in self.map_gui.children:
                    child.enable_colour_of_type = map.matrix[child.row][child.col].cell_type
                    child.set_cell()

                    #Defaults selected cell assignment back to CellType.PATH
                    child.enable_colour_of_type = CellType.PATH
        except:
            error_popup = Popup(size_hint=(None, None), size=(250, 60), title='Error:  Not a serialized map file', title_align='center', auto_dismiss=True, separator_height=0)
            error_popup.open()

        self.file_chooser_popup.dismiss()



    def create_serialization_success_popup(self):
        """Creates the successful serialization popup.

        Args:
            NONE

        Returns:
            NONE
        """
        popup = Popup(size_hint=(None, None), size=(120, 60), title='Saved', title_align='center', auto_dismiss=True, separator_height=0)

        return popup



    def disable_window_resize(self, x, y, instance=None):
        """Disables window resizing.

        Args:
            instance - N/A
            x - The window's current width.
            y - The window's current height.

        Returns:
            NONE
        """
        if x != window_x or y != window_y:
            Window.size = (window_x, window_y)



#MAIN
if __name__ == '__main__':
    MappingUtilApp().run()