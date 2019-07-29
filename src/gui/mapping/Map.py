from src.gui.mapping.Cell import Cell
from src.gui.mapping.CellType import CellType

class Map:

    def __init__(self, rows, cols):
        """Constructor.

        Args:
            rows - Number of rows.
            cols - Number of columns.

        Returns:
            NONE
        """
        self.rows = rows
        self.cols = cols
        self.matrix = [[None for col in range(cols)] for row in range(rows)]



    def print_map(self):
        """Prints the map.

        Args:
            NONE

        Returns:
            NONE
        """
        for row in range(self.rows):
            for col in range(self.cols):
                print(str(self.matrix[row][col].cell_type) + ': ' + '(' + str(self.matrix[row][col].row) + ', ' + str(self.matrix[row][col].col) + ')')