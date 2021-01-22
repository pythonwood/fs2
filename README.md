# fscmd

### [fscmd](https://github.com/pythonwood/fscmd/) is a cmd tool based on [pyfilesystem2](https://github.com/PyFilesystem/pyfilesystem2)

### Usage

    Usage: fscmd [OPTIONS] COMMAND [ARGS]...
    
      This script is pyfilesystem2 command line tool.
    
      example:
          fscmd ls .
          fscmd -u file://c:/windows ls system32
          fscmd -u zip:///tmp/a.zip ls /
          fscmd -u tar:///etc/bak.tar.gz  ls opkg config
          fscmd -u temp:// ls .
          fscmd -u s3:// ls .                                 # pip install fs-s3fs
          fscmd -u dropbox:// ls .                            # pip install fs.dropboxfs
          fscmd -u webdav://user:pass@127.0.0.1/web/dav/ ls . # pip install fs.webdavfs
          fscmd -u ssh://my.vps.com/home/ ls .                # pip install fs.sshfs
          fscmd --listopener                                  # list all support filesystem
    
      mutil url is supported:
          fscmd -u /tmp -u ssh://vps/tmp ls .
    
    Options:
      -l, --listopener  list supported file system
      -u, --url TEXT    filesystem url: default is "."
      --help            Show this message and exit.
    
    Commands:
      cat    read file and print content.
      cp     copy file (same fs).
      dl     download file to local disk.
      info   get info of resource.
      ls     list files and dirs.
      mkdir  create directory.
      mv     move file (same fs).
      rm     delete file and dirs.
      rmdir  get info of resource.
      tree   list files and dirs as tree view.
      up     upload local disk file to remote filesystem.

