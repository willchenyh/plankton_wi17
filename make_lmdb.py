import matplotlib
matplotlib.use('Agg')

import numpy as np
import cv2
import os, glob, random, caffe, lmdb
from caffe.proto import caffe_pb2

IMG_W = 256
IMG_H = 256

def make_datum(img,label):
    return caffe_pb2.Datum(
	channels=3,
	width=IMG_W,
	height=IMG_H,
	label=label,
	data=img.tostring())

def convert(imgf, labelf, n, lmdb_file):
    f = open(imgf, "rb")
    l = open(labelf, "rb")

    f.read(16)
    l.read(8)
    
    with lmdb_file.begin(write=True) as txn:
        for i in range(n):
            label = ord(l.read(1))
	    #print label, type(label[0])
   	    image = np.zeros((28,28),np.uint8)
            '''
	    while image_bytes:
	        img_uc = struct.unpack("=784B", image_bytes)
	        for j in range(28*28):
		    image.itemset(j, img_uc[j])
  	    ''' 
            for j in range(28*28):
	        c = ord(f.read(1))
                image.itemset(j, c)
	    #print c
	    image = cv2.resize(image, (256,256))
	    image2 = cv2.merge((image, image, image))
	    #print image2
	    datum = make_datum(image2, label)
	    txn.put('{:0>5d}'.format(i), datum.SerializeToString())
    lmdb_file.close()
    '''
    for image in images:
        o.write(",".join(str(pix) for pix in image)+"\n")
    '''
    f.close()
    l.close()

 
train_lmdb = 'train_lmdb'
val_lmdb = 'val_lmdb'
in_db = lmdb.open(train_lmdb, map_size=int(1e12))
convert("train-images-idx3-ubyte", "train-labels-idx1-ubyte",
         60000, in_db)
in_db = lmdb.open(val_lmdb, map_size=int(1e12))
convert("t10k-images-idx3-ubyte", "t10k-labels-idx1-ubyte",
         10000, in_db)
