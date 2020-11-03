from .init import fs2, click, errors
from fs.path import relpath, normpath
import os,sys,time
import posixpath

def _rm(fs, path, vcount=0):
    fs.remove(path)
    if vcount >= 1:
        print(time.strftime('%F_%T'), 'rm %s' % path)


@fs2.command()
@click.argument('paths', nargs=-1)
@click.option('--force', '-f', is_flag=True, help='ignore nonexistent files and arguments, never prompt')
@click.option('--verbose', '-v', count=True, help='more info')
@click.option('--interactive', '-i', is_flag=True, help='prompt before every removal')
@click.option('--recursive', '-r', is_flag=True, help='remove directories and their contents recursively')
@click.pass_context
def rm(ctx, paths, force, verbose, interactive, recursive):
    if not force:
        click.confirm('delete is dangerous. Continue?', abort=True, default=True)
    fs = ctx.obj['fs']
    for path in paths:
        try:
            _rm(fs, path, verbose)
        except errors.FileExpected:
            if not recursive:
                click.confirm('%s is a dir, need --recursive/-r option. Continue?' % path, abort=True, default=True)
            tops = []
            for top, subs, files in fs.walk.walk(path):
                print(top, subs, files)
                for finfo in files:
                    target = posixpath.join(top, finfo.name)
                    if interactive:
                        click.confirm('delete %s. Sure?' % target, abort=True, default=True)
                    _rm(fs, target, verbose)
                tops.append(top)
            for top in tops[::-1]:
                fs.removedir(top)
                if verbose >= 1:
                    print(time.strftime('%F_%T'), 'rmdir %s' % top)
        except errors.ResourceNotFound:
            if not force:
                click.confirm('%s is not exist. Continue?' % path, abort=True, default=True)

