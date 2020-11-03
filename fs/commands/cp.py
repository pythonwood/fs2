from fs.path import relpath, normpath, abspath
import posixpath
import os,sys
import posixpath

from .init import fs2, click, errors
from .init import FS2_NOEXIST, FS2_ISFILE, FS2_ISDIR

@fs2.command()
@click.argument('src', nargs=-1)
@click.argument('dst', nargs=1)
@click.option('--recursive', '-r', is_flag=True, help='copy directories recursively')
@click.option('--force', '-f', is_flag=True, help='force overwrite if existing destination file')
@click.pass_context
def cp(ctx, src, dst, recursive, force):
    """Copy file from SRC to DST.
    ./fs2 cp tox.ini .
    ./fs2 cp tox.ini a.ini dir/ path/to/
    """
    fs = ctx.obj['fs']

    ### check dst part
    dst_is, dirlist = FS2_ISDIR, []
    try:
        dirlist = fs.listdir(dst)
        if not force:
            click.confirm('%s is an exist dir. Continue?' % dst, abort=True, default=True)
    except errors.DirectoryExpected:
        dst_is = FS2_ISFILE
        if not len(src) == 1 or not os.path.isfile(src[0]):
            click.echo('%s is a file so only one file is need' % dst)
            return
        if not force:
            click.confirm('%s is an exist file. Continue?' % dst, abort=True, default=True)
    except errors.ResourceNotFound:
        if len(src) == 1:
            dst_is = FS2_NOEXIST

    for fn in src:
        _dst = dst
        if dst_is == FS2_ISDIR:
            _dst = posixpath.join(dst,posixpath.basename(fn))
        try:
            fs.copy(fn, _dst, overwrite=force)
        except errors.ResourceNotFound:
            click.echo('parent dir not exists: %s' % posixpath.dirname(_dst))
            break


