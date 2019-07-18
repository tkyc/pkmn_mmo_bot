


class Cell:



    def __init__(self, x, y):
        """Constructor.

        Args:
            x - x-coordinate.
            y - y-coordinate.

        Returns:
            NONE
        """
        self.x = x
        self.y = y
        self.prop = False
        self.grass = False
        self.target = False
        self.path = False



    def set_prop(self, prop):
        """Sets prop boolean.

        Args:
            boolean - True if the cell is a prop. Otherwise, false.

        Return:
            NONE
        """
        self.prop = prop