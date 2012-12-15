import os
from os.path import join, islink

from celery.task import task

from models import db, FileEntry

@task
def scan_folder(path):
    """ This Celery task, scans a folder and all subfolders to get file information
         - make platform independent
         - avoid loops
         - use caching ????
    """
    # iterate folder contents
    for root, dirs, files in os.walk(path, followlinks=False):
        # iterate all files
        for name in files:
            file_path = join(root, name)
            try:
                save_file_meta(file_path)
            except Exception as e:
                # logger.debug("Unable to read file '%s', reason: '%s'" % (file_path, e))
                pass
                
        # iterate all directories
        for dir in dirs:
            folder_path = join(root, dir)
            try:
                save_file_meta(folder_path)
            except Exception as e:
                # logger.debug("Unable to read folder '%s', reason: '%s'" % (folder_path, e))
                print e
                pass
            # do not continue for symlicks, it will create loop
            if not islink(folder_path):
                scan_folder(folder_path)


def save_file_meta(path):
    statinfo = os.stat(path)
    # get readable creation date ?? no .. do this on view...
    # naive filetype assumption
    
    f_size = statinfo.st_size
    # platform dependent
    f_type = statinfo.st_type if hasattr(statinfo, "st_type") else ""
    f_date = statinfo.st_ctime
    f_date_last_update = statinfo.st_mtime
    
    # TODO look for bulk insertion, instead of one-by-one
    # create Database entry and save
    f = FileEntry(path, f_size, f_type, f_date, f_date_last_update)
    # check an eeficient way for add-or-update
    merged_object = db.session.merge(f)
    db.session.commit()
    
    print path
    