from enum import Enum


class PlotType(Enum):
    LINEAR = "linear"
    SEMILOG = "semi-logarithmic"
    LOG = "logarithmic"

class InputType(Enum):
    TABLE = "table"
    EXCEL = "excel"

