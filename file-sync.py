#!/usr/local/bin/python3

import pyinotify
import asyncio
# https://docs.python.org/2.5/dist/module-distutils.dirutil.html
from distutils.dir_util import mkpath,copy_tree,remove_tree
import datetime
import time
from os.path import isdir

# Directory to watch and copy when modified in any way
SRC = "./Google Drive/Projects"

# Directory to delete and replace with copied SRC contents
DEST = "./OneDrive/Projects"

def log(string = ""):
    timestamp = str(datetime.datetime.now())
    print(timestamp+" "+str(string))
    f = open("log.txt", "a")
    f.write(timestamp+" "+str(string)+"\r\n")

# Handles the event when the SRC directory is modified in any way
def handle_event(notifier=None):
    if notifier:
        log(SRC+" has been modified")
    log("SRC is: "+SRC)
    log("DEST is: "+DEST)
    log("SRC is being copied to DEST")

    try:
        backup = None
        start = time.time()
        
        # If the DEST destination exists
        if isdir(DEST):
            log("DEST already exists")

            # Name the backup destination
            backup = DEST+"-backup"

            # Create the backup destination
            log("Creating backup directory: "+backup)
            mkpath(backup)

            # Copy all of the files and folders in DEST directory to the backup directory
            log("Backing up DEST")
            copy_tree(DEST,backup)

            # Delete the DEST directory
            log("Deleting DEST")
            remove_tree(DEST)
        
        # Create the DEST directory
        log("Creating DEST")
        mkpath(DEST)

        # Copy all of the files and folders in SRC directory to the DEST directory
        log("Copying everything from SRC to DEST")
        copy_tree(SRC,DEST)
        log("SRC successfully copied to DEST")

        # If there are no exceptions and if a backup directory exists then it will now be deleted
        if backup:
            log("Deleting backup")
            remove_tree(backup)

        end = time.time()
        log("Finished in "+str(round(end-start,2))+" seconds")

    except Exception as e:
        log(e)

        if notifier:
            notifier.loop.stop()

try:
    if not isdir(SRC):
        raise Exception(SRC+" is not a directory")

    # Initialize by running the handle_event function
    handle_event()

    # Credit this snippit to https://github.com/seb-m
    # https://github.com/seb-m/pyinotify/blob/master/python3/examples/asyncio_notifier.py
    wm = pyinotify.WatchManager()
    loop = asyncio.get_event_loop()
    notifier = pyinotify.AsyncioNotifier(wm,loop,callback=handle_event)
    wm.add_watch(SRC,pyinotify.ALL_EVENTS)
    log()
    log("Watching "+SRC)
    loop.run_forever()
    notifier.stop()
            
except Exception as e:
    log(e)
    notifier.loop.stop()