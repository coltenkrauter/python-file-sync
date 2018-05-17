import pyinotify
import asyncio
# https://docs.python.org/2.5/dist/module-distutils.dirutil.html
from distutils.dir_util import mkpath,copy_tree,remove_tree
from os.path import isdir

# Directory to watch and copy when modified in any way
SRC = "./Google Drive/Projects"

# Directory to delete and replace with copied SRC contents
DEST = "./OneDrive/Projects"

# Handles the event when the SRC directory is modified in any way
def handle_event(notifier=None):
    try:
        backup = None

        # If the DEST destination exists
        if isdir(DEST):
            # Name the backup destination
            backup = DEST+"-backup"

            # Create the backup destination
            mkpath(backup)

            # Copy all of the files and folders in DEST directory to the backup directory
            copy_tree(DEST,backup)

            # Delete the DEST directory
            remove_tree(DEST)
        
        # Create the DEST directory
        mkpath(DEST)

        # Copy all of the files and folders in SRC directory to the DEST directory
        copy_tree(SRC,DEST)

        # If there are no exceptions and if a backup directory exists then it will now be deleted
        if backup:
            remove_tree(backup)

    except Exception as e:
        print(e)

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
    loop.run_forever()
    notifier.stop()
            
except Exception as e:
    print(e)
    notifier.loop.stop()
