def ExtractVarint(data, offset=0):
    if data[offset] == 0:
        return 0

    varint_length = 0
    varint_binary = ""
    #loop until the value of a byte is lower than 128
    for i in range(0, 9):
        varint_length += 1
        if ord(data[offset+i:offset+i+1]) < 128:
            break
    for i in range(varint_length):
        #transform the binary data(binary -> int -> bit representation (concat all results))
        varint_binary += format((ord(data[offset+i:offset+i+1])), '#010b')[3:]
    #transformate the bit represntation back into an integer
    return int(varint_binary, 2), varint_length
