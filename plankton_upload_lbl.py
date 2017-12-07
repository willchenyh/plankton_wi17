# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 13:40:35 2017

@author: kevin
"""

import sqlite3 as lite
import json, os, glob
import numpy as np
import datetime
from lxml import html
#import urllib 
import urllib2
import cookielib
import pandas as pd

def prorolbl_upload(proro_dict):
    '''
    csv file preprocessing for prorocentrum (optimized for multiple label uploads
    :param proro_dict: 
    :return: image id list and confidence level list
    '''
    TIMESTAMP_LIST = ['2017-3-20', '2017-3-27', '2017-4-10']
    plank_prorocentrum_root = '/data4/plankton_wi17/plankton/plankton_binary_classifiers/plankton_phytoplankton'

    for TIMESTAMP in TIMESTAMP_LIST:
        # Read in list of machine labels
        df = pd.read_csv (plank_prorocentrum_root + '/code/1_target_' + TIMESTAMP + '_image_path_labels.csv')

        # Get image id for each predicted prorocentrum (1)
        for index, row in df.iterrows ():
            if row['predictions'] == 1:
                proro_dict['images'].append (row['img_id'])
                # proro['confidence_list'].append(row['confidence_level']
        print TIMESTAMP + ' Total oithona labels: ' + str (len (proro_dict['images']))
    return proro_dict['images']

def targetlbl_upload():
    target_root = '/data4/plankton_wi17/mpl/target_domain'

    csv_filename = '/spcinsitu/insitu_finetune/exp2/insitu_finetune_preds.csv'
    df = pd.read_csv(target_root + csv_filename, index_col=0) # csv_file upload

    txt_filename = '/data4/plankton_wi17/plankton/compare_google_lab/copepod_order/spctarget/L2S_target_preds.txt'
    df1 = pd.read_csv(txt_filename,sep=',',index_col=0)

    # False negatives
    mislabel = df['img_id'][(df['img_label']=="[u'Copepod']") & (df['predictions']==1)].tolist()

    calanoid_id = df1['img_id'][df1['predictions']==0].tolist()
    calanoid_confidence = df1['confidence_level'][df1['predictions']==0].tolist()

    cyclopoid_id = df1['img_id'][df1['predictions']==1].tolist()
    cyclopoid_confidence = df1['confidence_level'][df1['predictions']==1].tolist()

    poecilo_id = df1['img_id'][df1['predictions']==2].tolist()
    poecilo_confidence = df1['confidence_level'][df1['predictions']==2].tolist()


    return calanoid_id, calanoid_confidence, cyclopoid_id, cyclopoid_confidence, poecilo_id, poecilo_confidence

def logintoserver():
    # Login to server
    cj = cookielib.CookieJar ()

    opener = urllib2.build_opener (
        urllib2.HTTPCookieProcessor (cj),
        urllib2.HTTPHandler (debuglevel=1)
    )

    login_url = 'http://spc.ucsd.edu/data/admin/?next=/data/admin'
    login_form = opener.open (login_url).read ()

    csrf_token = html.fromstring (login_form).xpath (
        '//input[@name="csrfmiddlewaretoken"]/@value'
    )[0]

    # make values dict
    values = {
        'username': 'kevin',
        'password': 'ceratium',
        # 'csrfmiddlewaretoken': csrf_token,
    }

    params = json.dumps (values)

    req = urllib2.Request ('http://spc.ucsd.edu/data/rois/login_user', params, headers={'X-CSRFToken': str (csrf_token),
                                                                                        'X-Requested-With': 'XMLHttpRequest',
                                                                                        'User-agent': 'Mozilla/5.0',
                                                                                        'Content-type': 'application/json'})
    resp = opener.open (req)
    print 'login ' + resp.read ()
    return opener, csrf_token



def upload_labels(lbl_dict, key, opener, csrf_token):
    lbl_json = json.dumps (lbl_dict)
    print 'done making json docs'

    # write the labels
    req1 = urllib2.Request ('http://spc.ucsd.edu/data/rois/label_images', lbl_json,
                            headers={'X-CSRFToken': str (csrf_token),
                                     'X-Requested-With': 'XMLHttpRequest',
                                     'User-agent': 'Mozilla/5.0',
                                     'Content-type': 'application/json'})
    resp1 = opener.open (req1)
    print key + ' labs: ' + str (len (resp1.read ()))



date = datetime.datetime.utcnow()
date = date.strftime('%s')
date1 = str(int(date)*1000)
date2 = str((int(date)*1000)-500)
# notes
# is machine
L2S_Calanoid = {"label":"Calanoid Copepod","tag":"","images":[],"is_machine":True,"confidence_list":[],"machine_name":"L2S_target_01","started": date2, "submitted": date1}
L2S_Cyclopoid = {"label":"Cyclopoid Copepod","tag":"","images":[],"is_machine":True,"confidence_list":[],"machine_name":"L2S_target_01","started": date2, "submitted": date1}
L2S_Poecilo = {"label":"Poecilostomatoid copepod","tag":"","images":[],"is_machine":True,"confidence_list":[],"machine_name":"L2S_target_01","started": date2, "submitted": date1}


L2S_Calanoid['images'], L2S_Calanoid['confidence_list'], L2S_Cyclopoid['images'], L2S_Cyclopoid['confidence_list'], L2S_Poecilo['images'], L2S_Poecilo['confidence_list'] = targetlbl_upload()
print(len(L2S_Calanoid['images']))
print(len(L2S_Cyclopoid['images']))
print(len(L2S_Poecilo['images']))

opener, csrf_token = logintoserver()
upload_labels(L2S_Calanoid,'L2S_Calanoid',opener, csrf_token)
upload_labels(L2S_Cyclopoid,'L2S_Cyclopoid',opener, csrf_token)
upload_labels(L2S_Poecilo,'L2S_Poecilo',opener, csrf_token)

# -------------------------------------------------------------------------------------- #

# mislabel_copepod_json = json.dumps (mislabel_copepod)
# print 'done making json docs'
#
# # Login to server
# cj = cookielib.CookieJar()
#
# opener = urllib2.build_opener(
#     urllib2.HTTPCookieProcessor(cj),
#     urllib2.HTTPHandler(debuglevel=1)
# )
#
# login_url = 'http://spc.ucsd.edu/data/admin/?next=/data/admin'
# login_form = opener.open(login_url).read()
#
# csrf_token = html.fromstring(login_form).xpath(
#     '//input[@name="csrfmiddlewaretoken"]/@value'
# )[0]
#
# # make values dict
# values = {
#     'username': 'kevin',
#     'password': 'ceratium',
#     #'csrfmiddlewaretoken': csrf_token,
# }
#
# params = json.dumps(values)
#
# req = urllib2.Request('http://spc.ucsd.edu/data/rois/login_user', params, headers={'X-CSRFToken': str(csrf_token),
#                                                                                    'X-Requested-With': 'XMLHttpRequest',
#                                                                                    'User-agent':'Mozilla/5.0',
#                                                                                    'Content-type': 'application/json'})
# resp = opener.open(req)
# print 'login ' + resp.read()
#
# # write the labels
# req1 = urllib2.Request('http://spc.ucsd.edu/data/rois/label_images', mislabel_copepod_json, headers={'X-CSRFToken': str(csrf_token),
#                                                                                    'X-Requested-With': 'XMLHttpRequest',
#                                                                                    'User-agent':'Mozilla/5.0',
#                                                                                    'Content-type': 'application/json'})
# resp1 = opener.open(req1)
# print 'Mislabel Copepod labs: ' + str(len(resp1.read()))

# make these all json docs:
"""
oith_json = json.dumps(oith)
para_json = json.dumps(para)
egg_json = json.dumps(egg)

print 'done making json docs'
# Login to server
cj = cookielib.CookieJar()

opener = urllib2.build_opener(
    urllib2.HTTPCookieProcessor(cj), 
    urllib2.HTTPHandler(debuglevel=1)
)

login_url = 'http://spc.ucsd.edu/data/admin/?next=/data/admin'
login_form = opener.open(login_url).read()

csrf_token = html.fromstring(login_form).xpath(
    '//input[@name="csrfmiddlewaretoken"]/@value'
)[0]


# make values dict
values = {
    'username': 'eric',
    'password': 'ceratium',
    #'csrfmiddlewaretoken': csrf_token,
}

params = json.dumps(values)

req = urllib2.Request('http://spc.ucsd.edu/data/rois/login_user', params, headers={'X-CSRFToken': str(csrf_token),
                                                                                   'X-Requested-With': 'XMLHttpRequest',
                                                                                   'User-agent':'Mozilla/5.0',
                                                                                   'Content-type': 'application/json'})
resp = opener.open(req)
print 'login ' + resp.read()
# write the labels
req1 = urllib2.Request('http://spc.ucsd.edu/data/rois/label_images', oith_json, headers={'X-CSRFToken': str(csrf_token),
                                                                                   'X-Requested-With': 'XMLHttpRequest',
                                                                                   'User-agent':'Mozilla/5.0',
                                                                                   'Content-type': 'application/json'})
resp1 = opener.open(req1)
print 'Oithona labs: ' + str(len(resp1.read()))

req2 = urllib2.Request('http://spc.ucsd.edu/data/rois/label_images', para_json, headers={'X-CSRFToken': str(csrf_token),
                                                                                   'X-Requested-With': 'XMLHttpRequest',
                                                                                   'User-agent':'Mozilla/5.0',
                                                                                   'Content-type': 'application/json'})
resp2 = opener.open(req2)
print 'Oithona labs: ' + str(len(resp2.read()))

req3 = urllib2.Request('http://spc.ucsd.edu/data/rois/label_images', egg_json, headers={'X-CSRFToken': str(csrf_token),
                                                                                   'X-Requested-With': 'XMLHttpRequest',
                                                                                   'User-agent':'Mozilla/5.0',
                                                                                   'Content-type': 'application/json'})
resp3 = opener.open(req3)
print 'Oithona labs: ' + str(len(resp3.read()))                                                                     
"""