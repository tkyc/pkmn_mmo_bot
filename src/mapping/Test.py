from kivy.app import App
from kivy.uix.widget import Widget
from Map import Map

map = Map(5, 5)


map.print_map()

map.matrix[0][0].set_prop(True)
print('\n')
map.print_map()