#!/usr/bin/env python

import os
import ast
import sys
from sys import version_info

try:
    import ConfigParser
except Exception:
    import configparser as ConfigParser

# Global
SETTING_FILE = 'dotfilesrc'
py3 = version_info[0] > 2

# Check if config file exist
if not os.path.exists(os.path.join(os.path.dirname(__file__), SETTING_FILE)):
    exit("config file not exists")

def get_setting():
    with open(os.path.join(os.path.dirname(__file__), SETTING_FILE)) as fp:
        config = ConfigParser.ConfigParser()
        config.readfp(fp)
        return config
    return None

def get_dots_as_list():
    config = get_setting()
    if not config:
        exit("no dotfiles")
    dots_config = config.get('dotfiles', 'dots')
    if not dots_config:
        exit("no dotfiles")
    try:
        dots = ast.literal_eval(dots_config) or []
    except ValueError:
        exit("no dotfiles")
    return dots

# sync dotfile listed in the config
# if the parent dir of a dotfile is not
# exist, it will be passed
def sync_dotfiles():
    if py3:
        response = input("Are you sure? [y/yes]: ")
    else:
        response = raw_input("Are you sure? [y/yes]: ")
    if not response.strip() == "y" and not response.strip() == "yes":
        exit("Bye")

    dots = get_dots_as_list()
    pwd = os.path.dirname(os.path.abspath(__file__))
    home = os.path.expanduser('~')

    for dot in dots:
        file_path = os.path.join(pwd, dot)
        dot_path = os.path.join(home, '.' + dot)
        if os.path.lexists(dot_path):
            continue
        try:
            os.symlink(file_path, dot_path)
        except Exception:
            pass
    exit("Done")

# remove a dotfile in here
def remove_dotfile(name):
    name_with_dot = '.' + name

    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), name)):
        exit("! not eixsts")

    dotpath = os.path.join(os.path.expanduser('~'), name_with_dot)
    if not os.path.lexists(dotpath):
        exit("Done, but you need to remove file manually")
    if not os.path.islink(dotpath):
        exit("! not a link")
    if os.path.realpath(dotpath) != os.path.join(os.path.dirname(os.path.abspath(__file__)), name.rstrip('/')):
        exit("! invalid action")

    # remove symlink in ~ directory
    try:
        os.unlink(dotpath)
    except:
        exit("error when remove symlink")

    # move files
    os.rename(os.path.join(os.path.dirname(os.path.abspath(__file__)), name.rstrip('/')), dotpath)

    dotfiles = get_dots_as_list()
    if name in dotfiles:
        dotfiles.remove(name)
        config = get_setting()
        if not config: pass 
        config.set("dotfiles", "dots", dotfiles)
        with open(os.path.join(os.path.dirname(__file__), SETTING_FILE), 'wb') as fp:
            config.write(fp)

    exit("Done")


# name is a dotfile in `~` directory
def add_dotfile(name):
    if py3:
        response = input("Are you sure? [y/yes]: ")
    else:
        response = raw_input("Are you sure? [y/yes]: ")
    if not response.strip() == "y" and not response.strip() == "yes":
        exit("Bye")

    if not name or len(name) is 0: exit()
    name = name if name[0] == '.' else '.' + name
    name_without_dot = name.lstrip('.')

    if os.path.islink(os.path.join(os.path.expanduser('~'), name)): 
        exit("! it already is a symlink")
    if not os.path.exists(os.path.join(os.path.expanduser('~'), name)): 
        exit("! not exists")
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), name_without_dot)): 
        exit("! already added, please sync dotfiles")

    # create folder in here if the path is not exists
    paths = name_without_dot.split('/')
    paths.pop()
    if len(paths):
        try:
            os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '/'.join(paths)))
        except:
            pass

    # copy files
    os.rename(os.path.join(os.path.expanduser('~'), name), os.path.join(os.path.dirname(os.path.abspath(__file__)), name_without_dot))
    # create symbolic link
    os.symlink(os.path.join(os.path.dirname(os.path.abspath(__file__)), name_without_dot), os.path.join(os.path.expanduser('~'), name))

    dotfiles = get_dots_as_list()
    if name_without_dot not in dotfiles:
        dotfiles.append(name_without_dot)
        config = get_setting()
        if not config: pass 
        config.set("dotfiles", "dots", dotfiles)
        with open(os.path.join(os.path.dirname(__file__), SETTING_FILE), 'wb') as fp:
            config.write(fp)

    exit("Done")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        sync_dotfiles()
    elif len(sys.argv) > 2 and sys.argv[1][0] == '-' and sys.argv[1][1] == 'a':
        # add dotfile
        dotname = sys.argv[2]
        add_dotfile(dotname)
    elif len(sys.argv) > 2 and sys.argv[1][0] == '-' and sys.argv[1][1] == 'd':
        dotname = sys.argv[2]
        remove_dotfile(dotname)
    else:
        exit("./dotm.py | ./dotm.py -a [dotfile]")
