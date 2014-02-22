#!/usr/bin/env python

import subprocess
import time
import pygame
import datetime
import argparse

import pifacecommon
import pifacecad
from pifacecad.lcd import LCD_WIDTH

RIPITDIRTEMPLATE = "'\"/$artist/$album\"'"

class AutoRipper():
    def __init__(self,cdDrive,outputPath,timeout,cad):
        self.cdDrive = cdDrive
        self.outputPath = outputPath
        self.timeout = timeout
        self.cdDrive.init()

        # set up cad
        cad = pifacecad.PiFaceCAD()
        cad.lcd.blink_off()
        cad.lcd.cursor_off()
        cad.lcd.backlight_on()
        self.cad = cad

    def display(self,screen_message):
        self.display_lcd(screen_message,"")

    def display_lcd(self,screen_message,lcd_message):
        print screen_message
        print lcd_message


    def start(self):
        #open the cd drawer
        subprocess.call(["eject"])
        self.display("AutoRipper - Waiting for Audio Disk")
        #loop until a disk hasnt been inserted within the timeout
        lastTimeDiskFound = datetime.datetime.now()
        while (lastTimeDiskFound + datetime.timedelta(0,self.timeout)) > datetime.datetime.now():
            #is there a disk in the drive?
            if self.cdDrive.get_empty() == False:
                # Disk found
                # is it an audio cd?
                if self.cdDrive.get_track_audio(0) == True:
                    self.display("AutoRipper - Audio disk found, starting ripit.")
                    #run ripit
                    # getting subprocess to run ripit was difficult
                    #  due to the quotes in the --dirtemplate option
                    #   this works though!
                    ripit = subprocess.Popen("ripit --outputdir " + self.outputPath + " --dirtemplate=" + RIPITDIRTEMPLATE + " --nointeraction", shell=True)
                    ripit.communicate()
                    # rip complete - eject disk
                    self.display("AutoRipper - rip complete, ejecting")
                    # use eject command rather than pygame.cd.eject as I had problems with my drive
                    subprocess.call(["eject"])
                else:
                    self.display("AutoRipper - Disk inserted isnt an audio disk.")
                    subprocess.call(["eject"])
                lastTimeDiskFound = datetime.datetime.now()
                self.display("AutoRipper - Waiting for disk")
            else:
                # No disk - eject the tray
                subprocess.call(["eject"])
            # wait for a bit, before checking if there is a disk
            time.sleep(5)

        # timed out, a disk wasnt inserted
        self.display("AutoRipper - timed out waiting for a disk, quitting")
        # close the drawer
        subprocess.call(["eject", "-t"])
        #finished - cleanup
        self.cdDrive.quit()

if __name__ == "__main__":

    self.display("StuffAboutCode.com Raspberry Pi Auto CD Ripper")

    #Command line options
    parser = argparse.ArgumentParser(description="Auto CD Ripper")
    parser.add_argument("outputPath", help="The location to rip the CD to")
    parser.add_argument("timeout", help="The number of seconds to wait for the next CD")
    args = parser.parse_args()

    #Initialize the CDROM device
    pygame.cdrom.init()

    # make sure we can find a drive
    if pygame.cdrom.get_count() == 0:
        self.display("AutoRipper - No drives found!")
    elif pygame.cdrom.get_count() > 1:
        self.display("AutoRipper - More than 1 drive found - this isnt supported - sorry!")
    elif pygame.cdrom.get_count() == 1:
        self.display("AutoRipper - Drive found - Starting")
        autoRipper = AutoRipper(pygame.cdrom.CD(0),args.outputPath,int(args.timeout))
        autoRipper.start()

    #clean up
    pygame.cdrom.quit()
