from enum import Enum
from SQLRecord import *
from Common import ExtractVarint


class CellType(Enum):
    INTERIOR = 1
    LEAF = 2
    INVALID = 3


class SQLCell:
    base_offset = int
    type = CellType

    def parse(self, base_offset, data):
        pass

    def print(self):
        pass


class InteriorCell(SQLCell):
    type = CellType.INTERIOR
    child_page_number = int

    def parse(self, base_offset, data):
        self.base_offset = base_offset
        self.child_page_number = int.from_bytes(data[0:4], byteorder='big')

    def print(self):
        print("[InteriorCell] base_offset:", self.base_offset)
        print("[InteriorCell] child_page_number", self.child_page_number)


class LeafCell(SQLCell):
    type = CellType.LEAF
    length_of_record = int
    row_id = int
    record = Record

    def __init__(self):
        self.record = Record()

    def parse(self, base_offset, data):
        self.base_offset = base_offset
        try:
            self.record = Record()
            parse_base = 0
            self.length_of_record, length = ExtractVarint(data, parse_base)
            parse_base += length
            self.row_id, length = ExtractVarint(data, parse_base)
            parse_base += length
            self.record.parse(data[parse_base:parse_base+self.length_of_record])
        except:
            self.type = CellType.INVALID

    def print(self):
        if self.type != CellType.INVALID:
            print("[LeafCell] base_offset:", self.base_offset)
            print("[LeafCell] length_of_record:", self.length_of_record)
            print("[LeafCell] row_id:", self.row_id)
            self.record.print()
        #else:
        #    print("[LeafCell] Invalid Cell Detected")
