import sys
from ArchiveUnpacker import ArchiveReader

if len(sys.argv) == 1 :
    filepath = 'data.dat'
else:
    filepath = sys.argv[1]

if __name__ == '__main__':
    ArchiveReader(filepath)
