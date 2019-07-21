from CellType import CellType

class Cell:

    def __init__(self, row, col):
        """Constructor.

        Args:
            row - Row index of cell.
            col - Column index of cell.

        Returns:
            NONE
        """
        self.row = row
        self.col = col
        self.cell_type = None



    def set_cell_type(self, cell_type):
        """Sets cell type. Default is None.

        Args:
            cell_type - The cell type.

        Return:
            NONE
        """
        self.cell_type = cell_type