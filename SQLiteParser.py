from SQLHeader import *
from SQLPages import *
from SQLCell import *

# default setting
filename = "KakaoTalk2.db"

# open SQL File
f = open(filename, "rb")

# read SQL Header : 100byte
sql_header = SQLHeader()
result = sql_header.parse(f.read(100))
if result != 0:
    print("invalid file, errno:", result)
    exit(-1)
sql_header.print()
print()

# rewind
f.seek(0)

for i in range(sql_header.in_header_db_size):
    print(i, "th page")
    page_raw_data = f.read(sql_header.page_size)
    sql_page = SQLPage()
    sql_page.parse(sql_header.page_size * i, page_raw_data)
    sql_page.print()
    # parse cell
    sql_cell = SQLCell()
    if sql_page.type == SQLType.LEAF_INDEX or sql_page.type == SQLType.LEAF_TABLE:
        sql_cell = LeafCell()
    else:
        sql_cell = InteriorCell()
    for j in sql_page.cells_offset:
        sql_cell.parse(j, page_raw_data[j:])
        sql_cell.print()

    print()
