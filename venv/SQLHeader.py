from enum import Enum
# https://www.sqlite.org/fileformat.html
# 100-byte SQLite Header

magic_code = b'SQLite format 3' + b'\x00'  # 16byte


class SQLEncoding(Enum):
    UTF8 = 1
    UTF16_le = 2
    UTF16_be = 3


class SQLHeader:
    magic_code = bytearray
    page_size = int
    file_format_write_version = int
    file_format_read_version = int
    reserved_bytes_end_of_each_page = int
    must_be_64 = int
    must_be_32 = int
    must_be_32_2 = int
    file_change_counter = int
    in_header_db_size = int
    number_of_first_freelist_thunk_page = int
    total_number_of_freelist_pages = int
    schema_cookie = int
    schema_format = int
    page_cache_size = int
    number_of_largest_root_tree_page = int
    text_encoding = SQLEncoding
    user_version = int
    incremential_vacuum_mode = int
    application_id = int
    reserved_zero = bytearray(20)
    version_valid_for_number = int
    sqlite_version_number = int

    def parse(self, data):
        if len(data) < 100:
            return -1
        self.magic_code = data[0:16]
        # validate magic_code
        if self.magic_code != magic_code:
            return -2
        self.page_size = int.from_bytes(data[16:18], byteorder='big')
        self.file_format_write_version = data[18]
        self.file_format_read_version = data[19]
        self.reserved_bytes_end_of_each_page = data[20]
        self.must_be_64 = data[21]
        self.must_be_32 = data[22]
        self.must_be_32_2 = data[23]
        self.file_change_counter = int.from_bytes(data[24:28], byteorder='big')
        self.in_header_db_size = int.from_bytes(data[28:32], byteorder='big')
        self.number_of_first_freelist_thunk_page = int.from_bytes(data[32:36], byteorder='big')
        self.total_number_of_freelist_pages = int.from_bytes(data[36:40], byteorder='big')
        self.schema_cookie = int.from_bytes(data[40:44], byteorder='big')
        self.schema_format = int.from_bytes(data[44:48], byteorder='big')
        self.page_cache_size = int.from_bytes(data[48:52], byteorder='big')
        self.number_of_largest_root_tree_page = int.from_bytes(data[52:56], byteorder='big')
        self.text_encoding = SQLEncoding(int.from_bytes(data[56:60], byteorder='big'))
        self.user_version = int.from_bytes(data[60:64], byteorder='big')
        self.incremential_vacuum_mode = int.from_bytes(data[64:68], byteorder='big')
        self.application_id = int.from_bytes(data[68:72], byteorder='big')
        self.reserved_zero = data[72:92]
        self.version_valid_for_number = int.from_bytes(data[92:96], byteorder='big')
        self.sqlite_version_number = int.from_bytes(data[96:100], byteorder='big')
        return 0

    def print(self):
        print("[SQLHeader] magic_code:", self.magic_code)
        print("[SQLHeader] page_size:", self.page_size)
        print("[SQLHeader] file_format_write_version:", self.file_format_write_version)
        print("[SQLHeader] file_format_read_version:", self.file_format_read_version)
        print("[SQLHeader] reserved_bytes_end_of_each_page:", self.reserved_bytes_end_of_each_page)
        print("[SQLHeader] must_be_64:", self.must_be_64)
        print("[SQLHeader] must_be_32:", self.must_be_32)
        print("[SQLHeader] must_be_32_2:", self.must_be_32_2)
        print("[SQLHeader] file_change_counter:", self.file_change_counter)
        print("[SQLHeader] in_header_db_size:", self.in_header_db_size)
        print("[SQLHeader] number_of_first_freelist_thunk_page:", self.number_of_first_freelist_thunk_page)
        print("[SQLHeader] total_number_of_freelist_pages:", self.total_number_of_freelist_pages)
        print("[SQLHeader] schema_cookie:", self.schema_cookie)
        print("[SQLHeader] schema_format:", self.schema_format)
        print("[SQLHeader] page_cache_size:", self.page_cache_size)
        print("[SQLHeader] number_of_largest_root_tree_page:", self.number_of_largest_root_tree_page)
        print("[SQLHeader] text_encoding:", self.text_encoding)
        print("[SQLHeader] user_version:", self.user_version)
        print("[SQLHeader] incremential_vacuum_mode:", self.incremential_vacuum_mode)
        print("[SQLHeader] application_id:", self.application_id)
        print("[SQLHeader] reserved_zero:", self.reserved_zero)
        print("[SQLHeader] version_valid_for_number:", self.version_valid_for_number)
        print("[SQLHeader] sqlite_version_number:", self.sqlite_version_number)
