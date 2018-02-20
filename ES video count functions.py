# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 09:21:12 2017

@author: aperez

Quick functions for processing videos captured with the HID Mobile Capture Andriod App
"""

import os
import glob
#import pygame
import shutil
import pandas as pd
#from moviepy.editor import *
import cv2

def find_video_files(directory, subject_id = None, spoof_id = None):
    '''
    Finds all the mp4 video files in a directory. If subject_id is used, then 
    returns only video files of that subject id. 
    Returns a list.
    '''
    if subject_id is not None:
        return glob.glob(os.path.join(directory+'\Sub'+str(subject_id)+'*.mp4'))
    elif spoof_id is not None:
        return glob.glob(os.path.join(directory+'\*_Spf'+str(spoof_id)+'*.mp4'))
    else:
        return glob.glob(os.path.join(directory+'\*.mp4'))

def find_all_files(directory, subject_id = None):
    '''
    Finds all the folders and mp4 files in a directory collected with the HID app.
    If subject_id is used, then returns files for only that subject id.
    Returns a list.
    '''
    if subject_id is None:
        return glob.glob(os.path.join(directory+'\Sub*'))
    else:
        return glob.glob(os.path.join(directory+'\Sub'+str(subject_id)+'*'))
    
    
def count_videos(directory, file_type = None):
    '''
    Counts all the files or videos in a directory by subject id.
    Returns a dataframe of counts.
    '''
    video_files = find_all_files(directory)
        
    video_df = pd.DataFrame(video_files, columns=['path'])
    video_df['video_file'] = video_df['path'].str.split('\\').str[-1]
    video_df['subject_id'] = video_df['video_file'].str.split('_').str[0].str.split('Sub').str[-1]
    video_df['device_id'] = video_df['video_file'].str.split('_').str[1].str.split('Dev').str[-1]
    video_df['file_type'] = video_df['video_file'].str.split('.').str.len()
    video_df.set_value(video_df[video_df['file_type'] == 1].index, 'file_type', 'folder')
    video_df.set_value(video_df[video_df['file_type'] == 2].index, 'file_type', 'video')
    
    video_counts = pd.DataFrame(video_df[video_df['file_type'] == 'video']['subject_id'].value_counts())
    video_counts['folder'] = pd.DataFrame(video_df[video_df['file_type'] == 'folder']['subject_id'].value_counts())
    video_counts['total'] = pd.DataFrame(video_df['subject_id'].value_counts())
    video_counts.columns = ['videos', 'folders', 'total']
    video_counts.sort_index(inplace=True)
    
    return video_counts
    
def count_phones(day):
    '''
    Counts alls files in one day on all devices.
    Returns a pd df with these counts.
    '''    
    flag = True    
    devices = glob.glob(os.path.join(r'W:\External_Study_10-17-2017\Phones\*'))    
    for device in devices:
        if flag == True:
            video_counts = count_videos(device + r'\\' + day)
            flag = False
        else:
            video_counts = video_counts.add(count_videos(device + r'\\' + day), fill_value = 0)
    return video_counts

def count_days():
    '''
    Counts all files in all days over all devices.
    Returns a df of these counts.
    '''
    flag = True
    days = glob.glob(os.path.join(r'W:\External_Study_10-17-2017\Phones\Nexus_6P_84B7N16328000045\*'))
    
    for day in days:
        day = day.split('\\')[-1]
        if flag == True:
            all_count = count_phones(day)
            flag = False
        else:
            all_count = all_count.add(count_phones(day), fill_value = 0)
    return all_count

def play_video(video_file):
    '''
    Plays a mp4 video file. Does not return anything.
    '''
    video_clip = VideoFileClip(video_file)
    video_clip.preview(fps=5)
    pygame.display.quit()
    
    
def get_video_frames(video_file, directory):
    '''
    Takes a video_file and writes all frames in the video to directory.
    Returns nothing.
    '''
    video_path, video_name = os.path.split(video_file)
    print('Extracting:', video_name)
    save_path = os.path.join(directory, video_name[:-4])
    frame_name = os.path.join(save_path, video_name[:-4])    
    os.mkdir(save_path)
    
    video_capture = cv2.VideoCapture(video_file)
    success, frame = video_capture.read()
    count = 0
    success = True
    while success:
        success, image = video_capture.read()
        cv2.imwrite(frame_name + '_%d.jpg' % count, image)
        count += 1
    
def get_some_video_frames(video_file, directory, num_of_frames):
    '''
    Takes a video_file and writes all frames in the video to directory.
    Returns nothing.
    '''
    video_path, video_name = os.path.split(video_file)
    print('Extracting:', video_name)
    save_path = os.path.join(directory, video_name[:-4])
    frame_name = os.path.join(save_path, video_name[:-4])    
    os.mkdir(save_path)
    
    video_capture = cv2.VideoCapture(video_file)
    success, frame = video_capture.read()   
    count = 0
    total_frames = 900
    while success:
        success, image = video_capture.read()        
        if count in range(num_of_frames, total_frames, int(total_frames/num_of_frames)+1):
            cv2.imwrite(frame_name + '_%d.jpg' % count, image)
        count += 1       
        
def play_video_list(video_list):
    '''
    Plays video file list. Returns nothing.
    '''
    for video_file in video_list:
        print('Playing:', video_file.split('\\')[-1])
        play_video(video_file)    
        
def delete_files(video_list):
    '''
    Deletes mp4 files and folders with the same name in video_list.
    Returns nothing.
    '''
    for video_file in video_list:
        print('Deleting:', video_file.split('\\')[-1])
        os.remove(video_file)
        shutil.rmtree(video_file[:-4])
        
def correct_subject_id(video_file, correct_id):
    '''
    Changes the subject id in a file to the correct id. File extenstion does not 
    matter.
    Returns file with correct subject id.
    '''    
    video_path, video_name = os.path.split(video_file)
    correct_name = 'Sub'+str(correct_id)+video_name[video_name.find('_'):]    
    return os.path.join(video_path, correct_name)

def correct_spoof_id(video_file, correct_id):
    '''
    Changes the incorrect spoof id in a file to the correct id. File extenstion does not 
    matter. Returns file with correct subject id as str. 
    '''
    video_path, video_name = os.path.split(video_file)
    video_name_split = video_name.split('_')
    video_name_split[3] = video_name_split[3][:3]+str(correct_id)
    correct_name = '_'.join(video_name_split)
    return os.path.join(video_path, correct_name)
    
def rename_list(video_list, correct_id, spoof = False):
    '''
    Changes the subject or spoof id in a file list, and renames the file.
    Returns nothing.
    '''
    for video_file in video_list:
        if spoof:
            os.rename(video_file, correct_spoof_id(video_file, correct_id))
        else:
            os.rename(video_file, correct_subject_id(video_file, correct_id))

def rename_folder(folder, correct_id, spoof = False):
    '''
    Renames a folder and the contents of the folder.  
    Returns nothing.
    '''
    
    file_list = glob.glob(os.path.join(folder+'\*'))
    rename_list(file_list, correct_id, spoof)
    if spoof:
        os.rename(folder, correct_spoof_id(folder, correct_id))
    else:    
        os.rename(folder, correct_subject_id(folder, correct_id))
   
def rename_video(video_file, correct_id, spoof = False):
    '''
    Renames video file and matching folder (inclduing contents)
    Returns nothing.
    '''
    print('Renaming:', video_file.split('\\')[-1][:-4])
    if spoof:
        rename_folder(video_file[:-4], correct_id, True)
        os.rename(video_file, correct_spoof_id(video_file, correct_id))
    else:
        rename_folder(video_file[:-4], correct_id)
        os.rename(video_file, correct_subject_id(video_file, correct_id))

# Paths to directories removed for privacy.
VIDEO_DIRECTORY = r''
SAVE_DIRECTORY = r''
SPOOF = False
SPOOF_ID = None
CORRECT_ID = 4

video_list = find_video_files(VIDEO_DIRECTORY)
for video_file in video_list:
    get_some_video_frames(video_file, SAVE_DIRECTORY, 33)