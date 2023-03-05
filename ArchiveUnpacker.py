import zlib
import os
import struct
import io

HEADER = "ArchiveFile"


def ArchiveReader(filepath):
    infor_list = []
    if not os.path.exists(filepath):
        raise Exception('文件不存在')
    fp_raw = open(filepath, mode='rb')
    fp_header = fp_raw.read(11).decode(encoding='utf8')
    if fp_header != HEADER:
        raise Exception('文件头错误')
    file_count = struct.unpack('i', fp_raw.read(4))[0]
    is_compressed = struct.unpack('b', fp_raw.read(1))[0]
    entry_size = struct.unpack('i', fp_raw.read(4))[0]

    if is_compressed:
        compressed_data = fp_raw.read(entry_size)
        data = decompress(compressed_data)
    else:
        # 基本不会有这种情况
        data = fp_raw.read(entry_size)
    data_stream = io.BytesIO(data)

    for i in range(file_count):
        EntryRecordSize = struct.unpack('i', data_stream.read(4))[0]
        dir_size = struct.unpack('i', data_stream.read(4))[0]
        if dir_size > 0:
            dir_name = struct.unpack(str(dir_size * 2) + 's', data_stream.read(dir_size * 2))[0].decode('utf-16le')
        else:
            dir_name = None
        name_size = struct.unpack('i', data_stream.read(4))[0]
        name = struct.unpack(str(name_size * 2) + 's', data_stream.read(name_size * 2))[0].decode('utf-16le')
        CompressType = struct.unpack('i', data_stream.read(4))[0]
        size_data = struct.unpack('i', data_stream.read(4))[0]
        size_compressed = struct.unpack('i', data_stream.read(4))[0]
        offset = struct.unpack('i', data_stream.read(4))[0]
        info = (EntryRecordSize, dir_size, dir_name, name_size, name, CompressType, size_data, size_compressed, offset)
        #            0               1          2        3        4        5            6           7              8
        # print('offset:', hex(offset))
        infor_list.append(info)

    for info in infor_list:
        path = info[2]
        if info[2] is not None: path = "output\\" + path
        else: path = 'output\\'
        if not os.path.exists(path): os.makedirs(path)
        fp_raw.seek(info[8])
        file_data = fp_raw.read(info[6])

        print(info)

        if info[5] == 1:
            file_data = decompress(file_data)
        with open(path+info[4], 'wb') as f:
            f.write(file_data)
    fp_raw.close()


def decompress(compressed_data):
    zobj = zlib.decompressobj()
    return zobj.decompress(compressed_data)


