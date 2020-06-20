from enum import Enum
from Common import ExtractVarint


class RecordType(Enum):
    invalid = -1
    NULL = 0
    int_8bit = 1
    int_16bit = 2
    int_24bit = 3
    int_32bit = 4
    int_48bit = 5
    int_64bit = 6
    float_64bit = 7
    zero = 8
    one = 9
    reserved = 10
    reserved_2 = 11
    blob = 12
    string = 13


class Record:
    data_header_length = int
    field_info = []
    field_data = [RecordType, int]

    def __init__(self):
        self.field_info = []
        self.field_data = []

    def get_size(self, type):
        if type == RecordType.invalid:
            return 0
        elif type == RecordType.NULL:
            return 0
        elif type == RecordType.int_8bit:
            return 1
        elif type == RecordType.int_16bit:
            return 2
        elif type == RecordType.int_24bit:
            return 3
        elif type == RecordType.int_32bit:
            return 4
        elif type == RecordType.int_48bit:
            return 6
        elif type == RecordType.int_64bit:
            return 8
        elif type == RecordType.float_64bit:
            return 8
        elif type == RecordType.zero:
            return 0
        elif type == RecordType.one:
            return 0

    def parse(self, data):
        parse_base = 0
        self.data_header_length, length = ExtractVarint(data, parse_base)
        parse_base += length

        # parse field information
        while parse_base < self.data_header_length:
            #print("Wooh, parse_base is", parse_base, "dataheaderlen:", self.data_header_length)
            field_type, length = ExtractVarint(data, parse_base)
            if field_type >= 12:
                if field_type % 2 == 0:  # blob
                    field_size = (field_type-12)/2
                    field_type = RecordType.blob
                else:  # string
                    field_size = (field_type-13)/2
                    field_type = RecordType.string
            else:  # default types
                field_type = RecordType(field_type)
                field_size = self.get_size(field_type)
            tmp_field_info = [field_type, int(field_size)]
            self.field_info.append(tmp_field_info)
            parse_base += length

            # parse field data
            for tmp_field_info in self.field_info:
                tmp_field_data = data[parse_base:parse_base+tmp_field_info[1]]
                self.field_data.append(tmp_field_data)
                parse_base += tmp_field_info[1]

    def print(self):
        print("[SQLRecord] data_header_length:", self.data_header_length)
        print("[SQLRecord] field_info:", self.field_info)
        print("[SQLRecord] field_data:", self.field_data)

