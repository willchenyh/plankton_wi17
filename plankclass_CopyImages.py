import glob
import os
import shutil
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pandas as pd
import random

# ADD CLASS TO /data4/plankton_wi17/plankton/images_orig under format YYYYMMDD/00X/
# where X is the specimen found that day. If adding any classes, update CLASS_TOTAL in plank_PartitionDatset.py
HOME = '/data4/plankton_wi17/plankton/'
CLA_00 = ['20170131/001']
CLA_01 = ['20170217/001', '20170217/002', '20170130/001', '20170209/002', '20170223/002', '20170126/003', '20170203/001', '20170223/001', '20170207/001', '20170209/001', '20170207/002', '20170213/003', '20170214/002', '20170217/004', '20170224/010', '20170214/003', '20170214/005', '20170216/001', '20170224/004', '20170216/004', '20170217/006', '20170124/002', '20170213/001', '20170216/002', '20170217/003', '20170224/005', '20170224/012']
CLA_02 = ['20170206/002', '20170207/006', '20170221/002', '20170120/001', '20170221/001', '20170221/003', '20170221/004', '20170221/005', '20170130/003', '20170214/001', '20170126/002', '20170130/002', '20170131/002', '20170120/002', '20170124/001', '20170214/004']
CLA_03 = ['20170203/002', '20170209/003']
CLA_04 = ['20170207/003', '20170210/001']
CLA_05 = ['20170207/005']
CLA_06 = ['20170126/001']
CLA_07 = ['20170209/004', '20170210/002', '20170221/006', '20170221/007', '20170216/003', '20170224/002', '20170224/007', '20170224/011', '20170224/006', '20170224/008', '20170224/009', '20170213/002', '20170207/004']
CLA_08 = ['20170217/005', '20170224/001', '20170224/003', '20170206/001']

PLANKTON_CLASS = {
    'class00': CLA_00,
    'class01': CLA_01,
    'class02': CLA_02,
    'class03': CLA_03,
    'class04': CLA_04,
    'class05': CLA_05,
    'class06': CLA_06,
    'class07': CLA_07,
    'class08': CLA_08,
}

'''
3-16-17 
Suggestion to read timestamp file names for a text file instead of typing out in code the timestamp file names
'''
TRAIN_PART_PERCENT = 0.5
VAL_PART_PERCENT = 0.1
SKIP_PART_PERCENT = 0.1
DEBUG = True

def extractData():
    taxonomyBranch = ['class']
    csvFNames = ['/data4/plankton_wi17/plankton/{}_timestamp.csv'.format(i) for i in taxonomyBranch]  # Add file attachment to taxonomy
    for i, csvF in enumerate(csvFNames):
        df = pd.read_csv(csvF)

        # Format and clean up data
        df = df.dropna(how='any')   # Drop NaN values
        df_timeStamp = df['Timestamp: '].str.replace("-","\r")
        df_timeStamp = df_timeStamp.str.split('\r')
        df['MLClass'] = ['class{:02}'.format(i) for i in range(len(df))]

        # Convert to list
        specimenTimestamp = df_timeStamp.tolist()       # List of timestamps
        specimenClass = df['class'].tolist()  # List of classes
        specimenNum = df['# of Specimen:'].tolist()     # List of specimens per class
        mlClass = df['MLClass'].tolist()

        specimenTimestamp = [filter(None, i) for i in specimenTimestamp]    # Clean up empty values from split
        if verifyN_TStampVsSpecimen(specimenTimestamp,specimenNum):         # Check if Tstamp and specimens match up
            datasetDict = dict(zip(mlClass, specimenTimestamp))

        # Plot data
        plotData(specimenClass, specimenNum, 'class')

        return datasetDict

def verifyN_TStampVsSpecimen(tstamp,spec):
    if len(spec) == len(tstamp):
        print ("Timestamp and Specimen count verified")
        return True
    else:
        return False

def plotData(listClass, listN_Specimen, taxonomicLvl):
    '''
    Plot histogram and chart of specimens vs class
    :param listClass: list of classes
    :param listN_Specimen: list of specimens
    :param taxonomicLvl: string such as family, order, class
    :return: 
    '''
    fig = plt.figure (figsize=(8, 6))  # Set figure size
    ax1 = fig.add_subplot (2, 1, 1, adjustable='box', aspect=0.3)
    n, bins, patches, = ax1.hist (listN_Specimen, int (max (listN_Specimen)), facecolor='green')
    ax1.set_xlabel ('Number of Specimens per Class')
    ax1.set_ylabel ('Number of Classes')
    ax1.set_title ('Histogram of Classes vs Specimen on {} lvl'.format (taxonomicLvl))
    ax1.set_aspect ('auto')

    ax2 = fig.add_subplot (2, 1, 2)
    ax2.barh (range (len (listClass)), listN_Specimen, tick_label=listClass)
    ax2.set_yticklabels (listClass, fontsize=8)
    ax2.set_xlabel ('Number of Specimens per Class')
    ax2.set_ylabel ('Classes')
    ax2.set_aspect ('auto', adjustable='box')
    plt.savefig (taxonomicLvl + '_chart')

def partition_image(img_dir):
    dataset = [img for img in glob.glob(img_dir+'/*png')]
    dataset.sort()
    num_train = int(len(dataset) * TRAIN_PART_PERCENT)
    num_val = int(len(dataset) * VAL_PART_PERCENT)
    num_skip = int(len(dataset) * SKIP_PART_PERCENT)
    num_test = len(dataset) - num_train - num_val - (num_skip*2)
    skip1 = num_train+num_skip
    val_partition = num_train+num_skip+num_val
    skip2 = num_train+num_skip+num_val+num_skip
    for in_indx, img_path in enumerate(dataset):
        print in_indx
        train_path = os.path.join(img_dir,'train')
        val_path = os.path.join(img_dir,'val')
        test_path = os.path.join(img_dir,'test1')
        skip_path = os.path.join(img_dir,'skip')
        trash_path = os.path.join(img_dir,'trash')
        check_trainvaltest_path(train_path, val_path, test_path, skip_path, trash_path)
        if in_indx <= num_train: #store into training folder
            shutil.move(img_path, train_path)
            if DEBUG:
                print "moved to train " + str(num_train)
        elif in_indx > num_train and in_indx <= skip1:  #skip1
            shutil.move(img_path, skip_path)
            if DEBUG:
                print "skipped1 " + str(skip1)
        elif in_indx > skip1 and in_indx <= val_partition: #store into validation folder
            shutil.move(img_path, val_path)
            if DEBUG:
                print "moved to val " + str(val_partition)
        elif in_indx > val_partition and in_indx <= skip2: #skip2
            shutil.move(img_path, skip_path)
            if DEBUG:
                print "skipped2 " + str(skip2)
        elif in_indx > skip2 and in_indx <= len(dataset): #store into testing folder
            shutil.move(img_path, test_path)
            if DEBUG:
                print "moved to test " + str(len(dataset))
    numTrainimg, numValimg, numTestimg = countImages([train_path, val_path, test_path])
    return numTrainimg, numValimg, numTestimg

def countImages(pathDirList):
    numImgList = range(len(pathDirList))
    for i, iPath in enumerate(pathDirList):
        imgList = glob.glob(iPath + '/*') # List of images
        numImgList[i] = len(imgList)
    return numImgList[0], numImgList[1], numImgList[2]

def check_trainvaltest_path(train_path,val_path,test_path,skip_path,trash_path):
    if not os.path.exists(train_path): 
        os.makedirs(train_path)
    if not os.path.exists(val_path):
        os.makedirs(val_path) 
    if not os.path.exists(test_path):
        os.makedirs(test_path)
    if not os.path.exists(skip_path):
        os.makedirs(skip_path)
    if not os.path.exists(trash_path):
        os.makedirs(trash_path)

def copy_image(class_dict, plankclasspath):
    '''
	CLASSPATH_LIST: List of class paths 
	plankclasspath: path to plankton classes
	'''
    for taxon_class, taxon_subclass in class_dict.items():
        for idx, timestamp_fn in enumerate(taxon_subclass):
            path_to_image = os.path.join('/data4/plankton_sp17/image_orig', timestamp_fn)
            if DEBUG:
                print "================================================================"
                print "class: " + str(taxon_class) + " /subclass" + str('{0:02}'.format(idx)) + " time_stampfn: " + str(
                    timestamp_fn)
                print "================================================================"
            pathList = glob.glob(os.path.join(path_to_image,'*'))
            if len(pathList) == 0:
                raise "EmptyList"
            index = range(len(pathList))
            random.shuffle(pathList)
            numImg = len(pathList)
            trainSet = pathList[:int(numImg*0.5)]
            unusedSet = pathList[int(numImg*0.5):int(numImg*0.6)]
            valSet = pathList[int(numImg*0.6):int(numImg*0.7)]
            unusedSet += pathList[int(numImg*0.7):int(numImg*0.8)]
            testSet = pathList[int(numImg*0.8):]
            partitions = ['train','val','test']
            destDir = os.path.join(plankclasspath, taxon_class,'subclass' + str('{0:02}'.format(idx)))
            for key in partitions:
                keyDir = os.path.join(destDir,key)
                if not os.path.exists(keyDir):
                    os.makedirs(keyDir)
            trainDir = os.path.join(destDir, 'train')
            valDir = os.path.join(destDir, 'val')
            testDir = os.path.join(destDir, 'test')
            symlinkFile(trainSet, trainDir)
            symlinkFile (valSet, valDir)
            symlinkFile (testSet, testDir)

def symlinkFile(pathList,destDir):
    for path in pathList:
        srcPath = path
        img = os.path.basename(path)
        destPath = os.path.join(destDir,img)
        if not os.path.exists(destPath):
            os.symlink(srcPath,destPath)

def copy_image_Tst():
    class1_subclass = [
        '20170217/002/',  # Copepoda;Calanoida;Acartia-class01
        '20170223/001/',  # Copepoda;Calanoida;II-class02
    ]
    class2_subclass = [
        '20170217/001/',  # Copepoda;Calanoida;Acartia-class01
    ]
    class_dict = {'class01': ['20170217/002/'], 'class02': class2_subclass}

    plankclasspath_tst = HOME + 'plankton_species/tst_images4/'
    print class_dict
    for key, value in class_dict.items():
        for idx, i in enumerate(value):
            if DEBUG:
                # print plankclasspath_tst
                print "class: " + str(key) + " /subclass" + str(idx) + " time_stampfn: " + str(i)
                copy_image(class_dict,plankclasspath_tst)
    image_database = glob.glob(plankclasspath_tst + '*')
    for class_idx,class_num in enumerate(image_database):
        subclass_fns = [os.path.join(class_num,fn) for fn in os.listdir(class_num)]
        for subclass_fn in subclass_fns:
            subclass_fn_parts = subclass_fn.split('/')
            subclass_idx = subclass_fn_parts[7]
            print subclass_fn
            print "================================================================"
            print "*                                                              *"
            print "* Partitioning                                                 *"
            print "*                                                              *"
            print "================================================================"
            partition_image(subclass_fn)

def main():
    plankClassDict = extractData()
    plankclasspath = HOME + 'plankton_class/labimages/'
    copy_image(plankClassDict, plankclasspath)
    exit(0)
    image_database = glob.glob(plankclasspath + '*')
    with open (class_num + '/stats.txt', "w") as f:
        for class_idx,class_num in enumerate(image_database):
            subclass_fns = [os.path.join(class_num,fn) for fn in os.listdir(class_num)]
            for subclass_fn in subclass_fns:
                subclass_fn_parts = subclass_fn.split('/')
                subclass_idx = subclass_fn_parts[7]
                nTrainimg, nValimg, nTestimg = partition_image(subclass_fn)
                trainList += nTrainimg
                valList += nValimg
                testList += nTestimg
            f.write('Class {} \n'.format(class_idx))
            f.write('\tTrain: {}'.format(len(trainList)))
            f.write('\tVal: {}'.format(len(valList)))
            f.write('\tTest: {}'.format(len(testList)))
            total = len(trainList) + len(valList) + len(testList)
            f.write('\tTotal: {}'.format(total))
    f.close()
if __name__ == '__main__':
# img_dir = HOME + 'testing_images/*tiff'
    main()
    plankclasspath = HOME + 'plankton_species/images/'
    #copy_image_Tst()
    #copy_image(PLANKTON_SPECIES, plankclasspath)
