import click
from fs import errors
from fs.path import relpath, normpath
import os,sys,time
import posixpath

def _rm(fs, path, vcount=0):
    fs.remove(path)
    if vcount >= 1:
        print(time.strftime('%F_%T'), 'rm %s' % path)


@click.command()
@click.argument('paths', nargs=-1)
@click.option('--force', '-f', is_flag=True, help='ignore nonexistent files and arguments, never prompt')
@click.option('--verbose', '-v', count=True, help='more info')
@click.option('--interactive', '-i', is_flag=True, help='prompt before every removal')
@click.option('--recursive', '-r', is_flag=True, help='remove directories and their contents recursively')
@click.pass_context
def rm(ctx, paths, force, verbose, interactive, recursive):
    """delete file and dirs.

    \b
    example:
        rm -f file1.txt pic.img
        rm -rf dir1/ dir2/
        rm -ri dir1/ dir2/
    """
    if not force:
        click.confirm('delete is dangerous. Continue?', abort=True, default=True)
    fs = ctx.obj['fs']
    for u,f in fs.items():
        fs_rm(f, paths, force, verbose, interactive, recursive)

def fs_rm(fs, paths, force, verbose, interactive, recursive):
    def fs_read_error(path, e):
        try:
            dirlist = fs.listdir(path)
            # for a/noexit1/noexit2/a.txt: must fs.makedirs('a/noexit1') before
            # fs.listdir('a/noexit1/noexit2'). otherwise ResourceNotFound 404.
            fs.makedirs(path)
            print(time.strftime('%F_%T'), 'WARN: %s should be dir because it has files, fixed.' % e)
        except errors.FSError:
            return False
        else:
            fs_rm(fs, paths=[posixpath.join(path, d) for d in dirlist], force=force,
                       verbose=verbose, interactive=interactive, recursive=recursive)
            return True # to ignore

    for path in paths:
        try:
            dirlist = fs.listdir(path)
            if not recursive:
                click.confirm('%s is a dir, need --recursive/-r option. Continue?' % path, abort=True, default=True)
            tops = []
            for top, subs, files in fs.walk.walk(path, on_error=fs_read_error):
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
        except errors.DirectoryExpected:
            _rm(fs, path, verbose)
        except errors.ResourceNotFound:
            if not force:
                click.confirm('%s is not exist. Continue?' % path, abort=True, default=True)

