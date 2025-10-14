flag_dec= open("./flag_dec.png", "wb+")

def file_encode(flag):
    i = 1
    while True:
        byte_str = flag.read(1)
        if (byte_str == b''):
            exit()
        byte_str = hex_encode(byte_str)
        file_write(flag_dec, byte_str)
        # print(byte_str, end="")
        i = i + 1

def hex_encode(byte_str):
    tmp = int.from_bytes(byte_str, byteorder="big")
    tmp=tmp^99
    if (tmp % 2 == 0):
        tmp = tmp + 1
    else:
        tmp = tmp - 1
    tmp = bytes([tmp])
    return tmp
    
def file_write(flag_dec, byte_str):
    flag_dec.write(byte_str)

if __name__ == '__main__':
    with open("./flag_enc.hex", "rb") as flag:
        file_encode(flag)
    flag_dec.close()
