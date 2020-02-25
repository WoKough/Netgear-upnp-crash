import sys
import socket
import time
import zlib
import struct

def main(filepath):
	with open(filepath, 'rb') as fpr:
		data = fpr.read()[0x46:]
	print("0x%x" % ((~zlib.crc32(data)) & 0xffffffff))

if __name__ == "__main__":
	main(sys.argv[1])