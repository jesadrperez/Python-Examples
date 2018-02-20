# -*- coding: utf-8 -*-
"""
Created on Fri Nov 09 09:51:54 2017

@author: aperez

Class to download and delete files from the Arlo website.
"""

import time
import os
from splinter import Browser
from bs4 import BeautifulSoup
import glob
import shutil

class Arlo_Site():
    '''
    Class used to download, and delete videos from Arlo webiste
    '''
    def __init__(self, site = None, date = None):
        '''
        Intiailizes class with password and email. If site and date are provided then
        sets those values.
        '''        
        self._site = site
        self._date = date        
        self._password = 'Intent2Detect'
        self._email = 'hmueller@hidglobal.com'        
        self._download_dir = r'C:\Users\aperez\Downloads'
        self._root_save_dir  = r'W:\Intent Detection'
        self._save_dir  = None        
        self._cameras_list = None
        
    def __str__(self):
        '''
        Print method, gives site and date in readable format.
        Returns str
        '''        
        info = 'Site: ' + self.get_site() + '\n'
        info += 'Date: ' + self.get_date() + '\n'
        info += 'Download Dir ' + self.get_download_dir() + '\n'
        if self.get_save_dir() != None:
            info += 'Save Dir: ' + self.get_save_dir() + '\n'
        if self.get_cameras_list() != None:            
            info += 'Cameras List: ' + self.get_cameras_list() + '\n'        
        return info
        
    def set_site(self, site = None):
        '''
        Prompts user for site.
        '''        
        if site == None:
            SITES = ['ABQ', 'Austin', 'Eden Prairie', 'Fremont', 'All Sites']    
            while True:
                site = raw_input('Choose site: \n 2 - Austin \n 3 - Eden Prairie \n 4 - Fremont \n')
                # Checks if valid Site Picked
                if (len(site) == 1):
                    break
                print 'Invalid Site Format.' 
            site = int(site)     
            site = SITES[site-1]
        self._site = site
        print 'Site set to:', site
           
    def set_date(self, date = None):
        '''
        Prompts user for date, and converts date to usable format.    
        '''
        if date == None:
            while True:
                date = raw_input('Enter date (e.g. 06-02-2017)'+'\n')
                # Automatically sets DATE to last workday 
                if (len(date) == 0):
                    date = time.localtime()
                    # Deals with Mondays
                    if date[6] == 0:
                        date = time.strftime("%m-%d-%Y", time.localtime(time.mktime(time.localtime())-3*86400))
                        break
                    # Last workday    
                    else:
                        date = time.strftime("%m-%d-%Y", time.localtime(time.mktime(time.localtime())-86400))    
                        break
                    break
                # Correct date format
                elif (len(date) == 10) and (date.find('-') != -1):
                    break
                # Reprompts user if date format is wrong.
                else:
                    print 'Invalid Date Format.'                   
        print 'Date set to:', date
        self._date = date
        
    def set_cameras(self, cameras_dict = None):
        ''' 
        Sets cameras based on site.
        '''
        if cameras_dict == None:
            if self.get_site() == 'Austin':
                self._cameras = {1:'/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[7]/div',
                           2:'/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[6]/div', 
                           3:'/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[5]/div', 
                           4:'/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[8]/div'}
            elif self.get_site() == 'Fremont':
                self._cameras = {1:'/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[9]/div',
                           2:'/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[11]/div', 
                           3:'/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[10]/div', 
                           4:'/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[12]/div'}    
            else: 
                self._cameras = {1:'/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[4]/div',
                           2:'/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div', 
                           3:'/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[3]/div', 
                           4:'/html/body/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div'}
        else:
            self._cameras = cameras_dict                
        
    def set_cameras_list(self, cameras_list):
        '''
        Sets camera list for camera to process. Default value is None and denotes to call cameras.
        Returns nothing.
        '''
        self._cameras_list = cameras_list
    
    def set_browser(self, browser):
        '''
        Sets browser
        '''        
        self._browser = browser
        
    def set_save_dir(self, save_dir):
        '''
        Sets save directory.
        '''
        self._save_dir = save_dir
        
    def set_root_save_dir(self, save_dir):
        '''
        Sets save directory.
        '''
        self._root_save_dir = save_dir        
        
    def set_download_dir(self, download_dir):
        '''
        Sets save directory.
        '''
        self._download_dir = download_dir
        
    def get_download_dir(self):
        '''
        Returns self._download_dir.
        '''
        return self._download_dir        
        
    def get_save_dir(self):
        '''
        Returns self._save_dir.
        '''
        return self._save_dir
    
    def get_root_save_dir(self):
        '''
        Returns self._save_dir.
        '''
        return self._root_save_dir
    
    def get_cameras(self):
        '''
        Returns dict of cameras.
        '''
        return self._cameras
    
    def get_site(self):
        '''
        Returns site as str
        '''
        return self._site             
        
    def get_date(self):
        '''
        Returns date as str.
        '''
        return self._date
    
    def get_password(self):
        '''
        Returns password as str.
        '''
        return self._password
    
    def get_email(self):
        '''
        Returns password as str.
        '''
        return self._email
    
    def get_cameras_list(self):
        '''
        Returns cameras_list.
        '''
        return self._cameras_list
    
    def get_browser(self):
        '''
        Returns browser
        '''
        return self._browser
    
    def update_save_dir(self):
        '''
        Updates save dir to reflect site, date and camera
        Returns nothing.
        '''
        # If cameras_list is None then sets to site and date only 
        if self.get_cameras_list() == None:
            self.set_save_dir(os.path.join(self.get_root_save_dir(), self.get_site(), self.get_date()))
        # If cameras_list more than one camera then sets to site and date only             
        elif len(self.get_cameras_list()) > 1:
            self.set_save_dir(os.path.join(self.get_root_save_dir(), self.get_site(), self.get_date()))
        # Adds site, date, and current camera to save path            
        else:            
            self.set_save_dir(os.path.join(self.get_root_save_dir(), self.get_site(), self.get_date(), 'Camera ' + str(self.get_cameras_list()[0])))        

    def open_broswer(self):
        '''
        Opens chrome browser goes to library page.
        Returns broswer.
        '''
        # Starts browser and goes to arlo site
        browser = Browser('chrome')
        browser.visit("https://arlo.netgear.com/#/login")            
        # Logs into website
        if browser.is_text_present('Support', wait_time=5):
            browser.fill('userId', self.get_email())
            browser.fill('password', self.get_password())
            button = browser.find_by_id('loginButton')
            button.click()            
        # Goes to arlo library
        if browser.is_text_present('Library',  wait_time=5):
            button = browser.find_by_id('footer_library')
            button.click()    
        self.set_browser(browser)
        
    def goto_date(self):
        '''
        Takes broswer to date
        Returns broswer
        '''
        date = self.get_date()
        browser = self.get_browser()        
        # Creates URL for specific date (format: https://arlo.netgear.com/#/calendar/201708/20170815/day)        
        calender_url = 'https://arlo.netgear.com/#/calendar/'+date[6:]+date[:2]+'/'+date[6:]+date[:2]+date[3:5]+'/day'    
        # Goes to page for date  
        browser.visit(calender_url)        
        self.set_browser(browser)
        
    def filter_cameras(self):
        '''
        Filters library by cameras, cameras_list is a int list for which cameras to filter by.
        If cameras_list is blank than all cameras are selected.
        Returns nothing.        
        '''        
        browser = self.get_browser()
        # Opens Filter settings
        if browser.is_text_present('Filter', wait_time=10):
            browser.find_by_xpath('//*[@id="arlo-header"]/div[2]/div/div[1]/span[2]').click()            
        # Goes to cameras
        if browser.is_text_present('Camera', wait_time=10):
            browser.find_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[2]').click()            
        # Sets to all cameras if cameras_list is None    
        if self.get_cameras_list() == None:
            self.set_cameras_list([1, 2, 3, 4])
        # Loops over camers in camera list
        for camera in self.get_cameras_list():
            if browser.is_text_present('Camera '+str(camera), wait_time=10):
                browser.find_by_xpath( self.get_cameras()[camera]).click()        
        # Saves Filter settings
        browser.find_by_id('libraryFilter_save').click()    
        self.set_browser(browser)
        
    def remove_filter(self):
        '''
        Removes camera filter.
        Returns nothing.
        '''
        self._browser.find_by_xpath('//*[@id="arlo-header"]/div[2]/div/div[1]/span[3]/span[2]').click()
        
    def count_online_videos(self):
        '''
        Counts the number of videos avaliable. 
        Returns the couint as a int.
        '''
        browser = self.get_browser()        
        # Clicks "Select"
        if browser.is_text_present('Select', wait_time = 10): 
           browser.find_by_xpath('//*[@id="arlo-header"]/div[2]/div/div[1]/span[4]/span').click()
        # Click "Select All"
        if browser.is_text_present('Select All', wait_time = 10):
            browser.find_by_xpath('//*[@id="arlo-header"]/div[2]/div/div[1]/span[4]/span[1]').click()   
        # Imports HTML to find number of videos
        soup = BeautifulSoup(browser.html, 'html.parser')
        num_vids = soup.find('span', {'class':'numOfSelected'})
        num_vids = num_vids.contents[0]
        num_vids = int(num_vids.split('(')[1].split(')')[0])                  
        # Clicks "Deslects All"
        browser.find_by_xpath('//*[@id="arlo-header"]/div[2]/div/div[1]/span[4]/span[1]').click()        
        # CLicks "Done"
        if browser.is_text_present('Done'):
            browser.find_by_xpath('//*[@id="arlo-header"]/div[2]/div/div[1]/span[4]/span[2]').click()        
        return num_vids
    
    def make_save_dir(self):
        '''
        Makes a folder for specific camera in the save directory.
        Returns nothing.
        '''        
        if not os.path.exists(self.get_save_dir()):
            os.makedirs(self.get_save_dir())

    def count_folder_videos(self):
        '''
        Counts the number of videos in the save_dir.
        Returns this count.
        '''                 
        if os.path.exists(self.get_save_dir()):
            return len(glob.glob(os.path.join(self.get_save_dir(), '*.mp4')))
        else:
            return 0
        
    def count_downloaded_videos(self):
        '''
        Counts the number of videos in the download_dir.
        Return this count.
        '''        
        return len(glob.glob(os.path.join(self.get_download_dir(), '*.mp4')))
    
    def move_videos(self):
        '''
        Moves videos from download dir to save dir
        Returns the number of saved videos
        '''
        downloaded_videos_list = glob.glob(os.path.join(self.get_download_dir(), '*.mp4'))
        for file in downloaded_videos_list:
            shutil.move(file, self.get_save_dir())
        return len(downloaded_videos_list)

    def delete_online_videos(self):
        '''
        Delete all videos in current library view.
        Returns nothing.
        '''
        browser = self.get_browser()
        num_videos = self.count_online_videos() 
        group_size = [50, 25, 12, 6, 3, 1]
        # Clicks "Select"
        if browser.is_text_present('Select', wait_time = 10): 
            browser.find_by_xpath('//*[@id="arlo-header"]/div[2]/div/div[1]/span[4]/span').click()            
        # Loops over group
        for group in group_size:
            # Breaks loop once all videos are deleted
            if num_videos == 0:
                break
            # Checks group size is corrent            
            while num_videos/group > 0:
                # Clicks on # of videos based on group                     
                for video in range(0, group):
                    # Clicks video    
                    browser.click_link_by_id('day_record_'+str(video))                
                # Deletes Videos
                if browser.is_text_present('Delete', wait_time = 10):
                    browser.find_by_xpath('//*[@id="arlo-footer"]/div[2]/div/div[5]').click()
                    browser.find_by_id('buttonConfirm').click()
                # Click confirmation                   
                if browser.is_text_present('Files were', wait_time = 60):
                    browser.find_by_xpath('/html/body/div[1]/div/div[2]/div[2]').click()
                # Waits to make sure videos are reloaded
                if browser.is_text_present('Select All', wait_time = 60):
                    time.sleep(5)
                    # Scrolls top of page
                    browser.execute_script("window.scrollTo(0, 0);")
                # Subtracts the number of videos deleted    
                num_videos -= group

    def download_videos(self):
        ''' 
        Downloads all videos in current library view.
        Returns nothing.
        '''
        browser = self.get_browser()
        # Counts number of videos avaliable for download
        num_videos = self.count_online_videos()
        # Clicks "Select"
        if browser.is_text_present('Select', wait_time = 10): 
            browser.find_by_xpath('//*[@id="arlo-header"]/div[2]/div/div[1]/span[4]/span').click()
        # Loops over videos            
        for video in range(0, num_videos):       
            # Clicks video    
            browser.click_link_by_id('day_record_'+str(video))
            # Downloads Video
            if browser.is_text_present('Download'):
                browser.find_by_xpath('//*[@id="arlo-footer"]/div[2]/div/div[4]').click()                
            # Unclicks video
            browser.click_link_by_id('day_record_'+str(video))
            # Pauses to avoid multiple downloads prompt
            time.sleep(0.5)
        # CLicks "Done"
        if browser.is_text_present('Done'):
            browser.find_by_xpath('//*[@id="arlo-header"]/div[2]/div/div[1]/span[4]/span[2]').click()
        # Pauses to allow videos to finish downloading
        time.sleep(30)
        browser.execute_script("window.scrollTo(0, 0);")

    def delete_download_videos(self):
        '''
        Deletes all the videos (.mp4s) in the download dir.
        Returns the number of videos deleted.
        '''
        downloaded_videos_list = glob.glob(os.path.join(self.get_download_dir(), '*.mp4'))
        for file in downloaded_videos_list:
            shutil.de(file, self.get_save_dir())
        return len(downloaded_videos_list)        
        
## Helper Functions

def start_arlo(site, date):
    '''
    Initaites arlo site instance
    arlo is a Arlo_Site class object
    site is a str
    date is a str
    Returns Arlo_Site.
    '''
    arlo = Arlo_Site(site, date)
    arlo.set_cameras()
    arlo.open_broswer()
    time.sleep(10)
    return arlo        
  

def delete_all_videos(arlo, dates_list):
    '''
    Deletes all videos in dates in dates_list. 
    dates_list is a list of dates
    Returns nothings
    '''
    for date in dates_list:
        arlo.set_date(date)
        arlo.goto_date()
        time.sleep(5)
        arlo.delete_online_videos()
        time.sleep()  

def download_site_daily_videos(arlo = None, site = None, date = None):
    '''
    Downloads all the videos for a site on a date on all 4 cameras.
    arlo is a Arlo_Site class object
    site is a str
    date is a str
    '''
    # Starts arlo site instance 
    if arlo == None:
        arlo = start_arlo(site, date)
    # Takes over initaited Arlo_Site instance
    else:
        arlo.set(site) 
        arlo.set_date(date)
    
    for camera in [1, 2, 3, 4]:
        arlo.set_cameras_list([camera])
        arlo.update_save_dir()
        arlo.make_save_dir()
        arlo.goto_date()
        time.sleep(10)
        arlo.filter_cameras()
        time.sleep(10)
        arlo.download_videos()
        print arlo.count_downloaded_videos()
        print arlo.move_videos()
        time.sleep(10)
        arlo.remove_filter()