from CellType import CellType
from Cell import Cell
import pickle

with open('serialized_map.config', 'rb') as serialized_map:
    map = pickle.load(serialized_map)

    for row in range(50):
        for col in range(50):
            # print('(' + str(map.matrix[row][col].row) + ', ' + str(map.matrix[row][col].col) + ')')
            print(str(map.matrix[row][col].cell_type) + ': ' + '(' + str(map.matrix[row][col].row) + ', ' + str(map.matrix[row][col].col) + ')')