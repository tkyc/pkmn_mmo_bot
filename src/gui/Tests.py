import pickle
from mapping.Cell import Cell
from mapping.CellType import CellType
from mapping.Map import Map

with open('serialized_map.config', 'rb') as serialized_map:
    map = pickle.load(serialized_map)
    map.print_map()