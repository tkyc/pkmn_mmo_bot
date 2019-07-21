from Cell import Cell

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
        self.matrix = [[Cell(row, column) for column in range(columns)] for row in range(rows)]



    def print_map(self):
        """Prints the map.

        Args:
            NONE

        Returns:
            NONE
        """
        for row in range(self.rows):
            for col in range(self.columns):
                print('[' + str(1 if self.matrix[row][col].prop else 0) + ']', end=' ')
                # print('(' + str(self.matrix[row][col].x) + ', ' + str(self.matrix[row][col].y) + ')', end=' ')
            print('\n')