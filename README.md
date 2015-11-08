# dotm

dotfile manager script

## Usage

Put this script file and `dotfilesrc` file in your dotfiles folder,
specific what dotfile do you want to manage in the `dotfiles` section
of the `dotfilesrc` file.

### Add a dotfile

A dotfile is located at `~` prefixed with a dot: `.`, like `.profile`, `.bashrc` etc. 

To add a dotfile, in the `dotfiles` which contains the `dotm.py` script:

``` bash
./dotm.py -a profile
```

this will add `~/.profile` file to your `dotfiles` folder with a name `profile` and add `profile` string to the `dotfilesrc` file.


### Remove a dotfile

To remove a dotfile, in the `dot files` which contains the `dotm.py` script:

``` bash
./dotm.py -a profile
```

this will unlink `~/.profile` symlink rename `profile` in the `dot files` folder to `~/.profile`.

---

(c) 2015 Towry Wang
