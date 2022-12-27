class Matrix:
    def __init__(self):
        self.matrix = []

    @classmethod
    def fill(cls, rows_number: int, columns_number: int, value=None):
        obj = cls()
        for i in range(rows_number):
            obj.matrix.append([])
            for j in range(columns_number):
                obj.matrix[-1].append(value)
