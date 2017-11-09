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

HOME = '/data4/plankton_wi17/plankton/'
DEBUG = True
def extractData():
    taxonomyBranch = ['family']
    csvFNames = ['/data4/plankton_wi17/plankton/plankton_family/{}_timestamp.csv'.format(i) for i in taxonomyBranch]  # Add file attachment to taxonomy
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
            # datasetDict = dict(zip(mlClass, specimenTimestamp))
            datasetDict = dict (zip (specimenClass, specimenTimestamp))

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

def countImages(pathDirList):
    numImgList = range(len(pathDirList))
    for i, iPath in enumerate(pathDirList):
        imgList = glob.glob(iPath + '/*') # List of images
        numImgList[i] = len(imgList)
    return numImgList[0], numImgList[1], numImgList[2]

def copy_image(class_dict, destpath):
    for taxon_class, taxon_subclass in class_dict.items ():
        for idx, timestamp_fn in enumerate(taxon_subclass):
            path_to_image = os.path.join ('/data4/plankton_sp17/image_orig', timestamp_fn)
            if DEBUG:
                print "================================================================"
                print "class: " + str (taxon_class) + " /subclass" + str (
                    '{0:02}'.format (idx)) + " time_stampfn: " + str (
                    timestamp_fn)
                print "================================================================"
            pathList = glob.glob (os.path.join (path_to_image, '*'))
            if len (pathList) == 0:
                raise "EmptyList"

def copypartition_image(class_dict, plankclasspath):
    '''
	CLASSPATH_LIST: List of class paths 
	plankclasspath: path to plankton classes
	'''
    # Initialization
    totalTrainimg = 0
    totalValimg = 0
    totalTestimg = 0
    with open('stats.txt','w') as f:
        for taxon_class, taxon_subclass in class_dict.items():
            totalTrainimg = 0
            totalValimg = 0
            totalTestimg = 0
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
                totalTrainimg += len(trainSet)
                totalValimg += len(valSet)
                totalTestimg += len(testSet)
            totalClassimg = totalTrainimg + totalValimg + totalTestimg
            f.write('{}\n'.format(taxon_class))
            f.write('\tTrain: {}\n'.format(totalTrainimg))
            f.write('\tVal: {}\n'.format(totalValimg))
            f.write('\tTest: {}\n'.format(totalTestimg))
            f.write('\tTotal: {}\n'.format(totalClassimg))
    f.close()

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
    print plankClassDict
    plankclasspath = HOME + 'plankton_family/labimages/'
    # copy_image(plankClassDict, plankclasspath)

if __name__ == '__main__':
    main()

