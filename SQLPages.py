import array
from enum import Enum


class SQLType(Enum):
    UNKNOWN = 1
    INTERIOR_INDEX = 2
    INTERIOR_TABLE = 5
    LEAF_INDEX = 10
    LEAF_TABLE = 13


class SQLPage:
    base_offset = int
    type = SQLType
    freeblock_addr = int
    number_of_cells = int
    first_cell_addr = int
    number_of_fragmented_free_bytes = int
    right_most_pointer = int
    cells_offset = []

    def __init__(self):
        self.cells_offset = []

    def parse(self, offset, data):
        parse_base = 0
        self.base_offset = offset
        # detect first page
        if self.base_offset == 0:
            parse_base += 100
        self.type = SQLType(data[parse_base])
        parse_base += 1
        self.freeblock_addr = int.from_bytes(data[parse_base:parse_base+2], byteorder='big')
        parse_base += 2
        self.number_of_cells = int.from_bytes(data[parse_base:parse_base+2], byteorder='big')
        parse_base += 2
        self.first_cell_addr = int.from_bytes(data[parse_base:parse_base+2], byteorder='big')
        if self.first_cell_addr == 0:
            self.first_cell_addr = 65536
        parse_base += 2
        self.number_of_fragmented_free_bytes = data[parse_base]
        parse_base += 1

        # validate interior page
        if self.type == SQLType.INTERIOR_INDEX or self.type == SQLType.INTERIOR_TABLE:
            self.right_most_pointer = int.from_bytes(data[parse_base:parse_base+4], byteorder='big')
            parse_base += 4

        # collect cells offset
        for i in range(self.number_of_cells):
            self.cells_offset.append(int.from_bytes(data[parse_base:parse_base + 2], byteorder='big'))
            parse_base += 2

    def print(self):
        print("[SQLPage] base_offset:", self.base_offset)
        print("[SQLPage] type:", self.type)
        print("[SQLPage] freeblock_addr:", self.freeblock_addr)
        print("[SQLPage] number_of_cells:", self.number_of_cells)
        print("[SQLPage] first_cell_addr:", self.first_cell_addr)
        print("[SQLPage] number_of_fragmented_free_bytes:", self.number_of_fragmented_free_bytes)
        if self.type == SQLType.INTERIOR_INDEX or self.type == SQLType.INTERIOR_TABLE:
            print("[SQLPage] right_most_pointer:", self.right_most_pointer)
        print("[SQLPage] cells_offset:", self.cells_offset)