from fs.path import relpath, normpath, abspath
import os,sys
import posixpath
import io

from .init import fs2, click, errors
from .init import FS2_NOEXIST, FS2_ISFILE, FS2_ISDIR

@fs2.command()
@click.argument('src', nargs=-1)
@click.argument('dst', nargs=1)
@click.option('--force', '-f', is_flag=True, help='force overwrite if existing destination file')
@click.pass_context
def dl(ctx, src, dst, force):
    """download file to local os
    example:
    dl . locdir/
    dl a.txt .
    dl a.txt loc/b.txt
    dl a.txt b.png c.mp3 dir/d/ remote/dir/
    """
    fs = ctx.obj['fs']

    ### check dst part
    dst_is, dirlist = FS2_ISDIR, []
    try:
        dirlist = os.listdir(dst)
        if not force:
            click.confirm('%s is an exist dir. Continue?' % dst, abort=True, default=True)
    except NotADirectoryError:
        dst_is = FS2_ISFILE
        if not force:
            click.confirm('%s is an exist file. Continue?' % dst, abort=True, default=True)
    except FileNotFoundError:
        if len(src) == 1:
            dst_is = FS2_NOEXIST
        else:
            os.makedirs(dst, exist_ok=True)
            dst_is = FS2_ISDIR

    ### check src part
    for fn in src:
        fn = abspath(fn)
        _dname, _fname = posixpath.split(fn)
        try:
            for top, subs, files in fs.walk.walk(fn):
                # dl remote/dir pathnoexist =>  remote/dir/a/b default to pathnoexist/dir/a/b
                _dst = posixpath.join(dst, top[len(_dname):].lstrip('/'))
                if dst_is == FS2_NOEXIST:
                    _dst = posixpath.join(dst, top[len(fn):].lstrip('/'))    # fix to pathnoexist/a/b
                try:
                    os.makedirs(_dst, exist_ok=force)
                except FileExistsError:
                    if not force:
                        click.confirm('%s is an exist dir. Continue?' % _dst, abort=True, default=True)
                for finfo in files:
                    with open(posixpath.join(_dst, finfo.name), 'wb') as f:
                        fs.download(posixpath.join(top, finfo.name), f)
        except errors.DirectoryExpected:
            _dst = dst
            if dst_is == FS2_ISDIR:
                _dst = posixpath.join(dst, posixpath.basename(fn))
            with open(_dst, 'wb') as f:
                fs.download(fn, f)
        except errors.ResourceNotFound:
            if not force:
                click.confirm('%s is not exist. Continue?' % fn, abort=True, default=True)

