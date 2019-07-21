from CellType import CellType
from Cell import Cell

m_cell = Cell(0, 0)
print(m_cell.cell_type)

m_cell.set_cell_type(CellType.TARGET)
print(m_cell.cell_type == CellType.TARGET)