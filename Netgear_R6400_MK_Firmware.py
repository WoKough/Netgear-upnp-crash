#!/usr/bin/python3

import binascii
import sys
import struct
import os

def crc32(filepath):
	with open(filepath, "rb") as fpr:
		content = fpr.read()
	#data = content[0x46:0x46+0x23aab6a-12]
	data = content[12:12+0x1e7f000]
	print("0x%x" % (binascii.crc32(data) & 0xffffffff))
	crc = binascii.crc32(data) ^ 0xffffffff
	print("~0x%x" % crc)
	return crc

def firm_pack():
	os.system("mksquashfs squashfs-root squashfs-root.squash -comp xz")
	with open("R6400-V1.0.1.52_1.0.36.chk", "rb") as fpr:
		content = fpr.read()
	header = content[0x3a:0x201d26]
	tail = content[0x01e7e210:]
	with open("squashfs-root.squash", "rb") as fprs:
		contents = fprs.read()
	with open("new-bin.chk", "wb") as fpw:
		fpw.write(header)
		fpw.write(contents)
		fpw.write(tail)
		lens = 0x1e7f000 - len(header) - len(contents) - len(tail)
		if lens > 0:
			for i in range(0,lens):
				fpw.write(struct.pack("b",0x0))

def patch_crc32(crc, filepath):
	with open(filepath, "rb") as fpr:
		content = fpr.read()
	with open(filepath, "wb") as fpw:
		fpw.write(content[:0x8])
		fpw.write(struct.pack("I", crc))
		fpw.write(content[0xc:])

def add_netgear_head(filepath):
	cmd = "./packet -k %s -f rootfs -b compatible_r6400.txt \
		-ok kernel -oall image -or rootfs -i ambitCfg.h" % filepath
	os.system(cmd)

if __name__ == '__main__':
	firm_pack()
	crc = crc32("new-bin.chk")
	patch_crc32(crc, "new-bin.chk")
	add_netgear_head("new-bin.chk")
