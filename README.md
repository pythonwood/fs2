# fs2

### [fs2](https://github.com/pythonwood/fs2/) is a cmd tool based on [pyfilesystem2](https://github.com/PyFilesystem/pyfilesystem2)

### Usage

    Usage: fs2 [OPTIONS] COMMAND [ARGS]...
    
      This script is pyfilesystem2 command line tool.
    
      example:
          fs2 ls .
          fs2 -u file://c:/windows ls system32
          fs2 -u zip:///tmp/a.zip tree /
          fs2 -u tar:///etc/bak.tar.gz  ls opkg config
          fs2 -u temp:// ls .
          fs2 -u s3:// ls .                                 # pip install fs-s3fs
          fs2 -u dropbox:// ls .                            # pip install fs.dropboxfs
          fs2 -u webdav://user:pass@127.0.0.1/web/dav/ ls . # pip install fs.webdavfs
          fs2 -u ssh://my.vps.com/home/ ls .                # pip install fs.sshfs
          fs2 --listopener                                  # list all support filesystem
    
      mutil url is supported:
          fs2 -u /tmp -u ssh://vps/tmp ls .
    
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

