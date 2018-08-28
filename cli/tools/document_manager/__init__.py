from __future__ import print_function, absolute_import

import os
import urllib
import contextlib
from os import listdir, remove, makedirs
import sys
from shutil import copyfile
cwd_root = ""
_cwd = os.getcwd()

def getcwd():
    global _cwd
    return _cwd

@contextlib.contextmanager
def cd(newdir):
    global _cwd
    prevdir = getcwd()
    os.chdir(newdir)
    _cwd = newdir
    try:
        yield
    finally:
        os.chdir(prevdir)
        _cwd = prevdir

def relpath(root, path): # relative path
    return path[len(root)+1:]

def mkdir(path):
    if not exists(path):
        makedirs(path)

def rmtree_readonly(directory):
    if os.path.islink(directory):
        os.remove(directory)
    else:
        def remove_readonly(func, path, _):
            os.chmod(path, stat.S_IWRITE)
            func(path)
        shutil.rmtree(directory, onerror=remove_readonly)

def delete_dir_files(directory):
    """ A function that does rm -rf

    Positional arguments:
    directory - the directory to remove
    """
    if not exists(directory):
        return

    for element in listdir(directory):
        to_remove = join(directory, element)
        if not isdir(to_remove):
            remove(to_remove)

def copy_file(src, dst):
    """ Implement the behaviour of "shutil.copy(src, dst)" without copying the
    permissions (this was causing errors with directories mounted with samba)

    Positional arguments:
    src - the source of the copy operation
    dst - the destination of the copy operation
    """
    if os.path.isdir(dst):
        _, base = os.path.split(src)
        dst = os.path.join(dst, base)
    copyfile(src, dst)          
            
def download_file(url, path):
    try:
    	urllib.urlretrieve(url, path)
    	return True
    except Exception as e:
    	print(e)
    	print("This file from %s can't be download"%(url))
    	sys.stdout.flush()
    	return False

def unzip(file, path):
	file_name = None
	try:
		pack = zipfile.ZipFile(file, "r")
		files = pack.namelist()
		file_name = files[0]
		pack.extractall(path)
		pack.close()
		return file_name
	except Exception:
		sys.exit(1)

def untar(file, path):
	file_name = None
	try:
		pack = tarfile.open(file, "r:gz")
		files = pack.getnames()
		file_name = files[0]
		for file in files:
			pack.extract(file, path)
		pack.close()
		return file_name
	except Exception as e:
		print(e)

def extract_file(file, path):
	extract_file_name = None
	extract_file_path = None
	filename, filesuffix = os.path.splitext(file)
	if filesuffix == ".gz":
		extract_file_name = untar(file, path)
	elif filesuffix == ".zip":
		extract_file_name = unzip(file, path)
	else:
		print("This file {} can't be extracted".format(file))
	if extract_file_name is not None:
		extract_file_path = os.path.join(path, extract_file_name)
	return extract_file_path

def show_progress(title, percent, max_width=80):
    if sys.stdout.isatty():
        percent = round(float(percent), 2)
        show_percent = '%.2f' % percent
        bwidth = max_width - len(str(title)) - len(show_percent) - 6 # 6 equals the spaces and paddings between title, progress bar and percentage
        sys.stdout.write('%s |%s%s| %s%%\r' % (str(title), '#' * int(percent * bwidth // 100), '-' * (bwidth - int(percent * bwidth // 100)), show_percent))
        sys.stdout.flush()
        
def hide_progress(max_width=80):
    if sys.stdout.isatty():
        sys.stdout.write("\r%s\r" % (' ' * max_width))

