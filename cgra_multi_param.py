from cgra_param import CGRAParam 


class MultiCGRAParam:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cgras = [[CGRAParam(r, c) for c in range(cols)] for r in range(rows)]