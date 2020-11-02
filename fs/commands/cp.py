from .init import fs2, click, errors
from fs.path import relpath, normpath

@fs2.command()
@click.argument('src', nargs=-1)
@click.argument('dst', nargs=1)
@click.option('--recursive', '-r', is_flag=True, help='copy directories recursively')
@click.option('--force', '-f', is_flag=True, help='force overwrite if existing destination file')
@click.pass_context
def cp(ctx, src, dst, recursive, force):
    """Copy file from SRC to DST.
    ./fs2 cp tox.ini tmp.ini
    """
    fs = ctx.obj['fs']
    url = ctx.obj['url']
    dst_is_dir, dirlist = True, []
    try:
        dirlist = fs.listdir(dst)
    except errors.DirectoryExpected:
        dst_is_dir = False
        if not len(src) == 1:
            # raise errors.Unsupported(msg='must overwrite a file with only one file')
            click.echo('%s is a file so only one src file is need' % dst)
            return
    except errors.ResourceNotFound:
        if len(src) == 1:
            dst_is_dir = False
    for fn in src:
        _dst = dst
        if dst_is_dir:
            _dst = posixpath.join(dst,posixpath.basename(fn))
        try:
            fs.copy(fn, _dst, overwrite=force)
        except errors.ResourceNotFound:
            click.echo('parent dir not exists: %s' % posixpath.dirname(_dst))
            break


