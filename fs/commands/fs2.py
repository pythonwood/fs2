#!/usr/bin/env python

import sys,os,time
import click
from fs import open_fs, errors
from fs.path import relpath, normpath, basename, dirname
import shutil
from fs.words2lines import words2lines
import posixpath

def _listopener():
    from fs.opener  import registry
    openers = set(registry.get_opener(i).__class__ for i in  registry.protocols)
    for opener in openers:
        print(str(opener), 'for', ['%s://' % i for i in opener.protocols])

@click.group(invoke_without_command=True) #https://click.palletsprojects.com/en/7.x/commands/#group-invocation-without-command
@click.option('--listopener', '-l', is_flag=True, help='list supported file system')
@click.option('--url', '-u', default='.', help='filesystem url: default is ".", eg. file:///tmp or webdav://user:pass@127.0.0.1/webdav/subdir/')
@click.pass_context
def fs2(ctx, listopener, url):
    # print(vars(ctx), listopener, url)
    if listopener:
        _listopener()
        return
    if not (ctx.args or ctx.invoked_subcommand):
        click.echo(ctx.get_help())
    if '://' not in url:
        url = 'file://' + url
    ctx.ensure_object(dict)
    ctx.obj['url'] = url
    ctx.obj['fs'] = open_fs(url)

@fs2.command()
@click.pass_context
def help(ctx):
    click.echo(ctx.parent.get_help()) # ctx.parent -> fs2 level

@fs2.command()
@click.argument('paths', nargs=-1, required=False) # 不限个数
@click.pass_context
def ls(ctx, paths):
    fs = ctx.obj['fs']
    url = ctx.obj['url']
    paths = paths or ['.']
    for path in paths:
        _path = path
        path = relpath(normpath(path))
        try:
            names = fs.listdir(path)
            if url.lower().startswith('file://') or url.lower().startswith('osfs://'):
                names.sort(key=lambda x: x.lstrip('.').lstrip('_').lower()) # sort as /bin/ls do
                # names = ['.', '..'] + names       # need not
            if len(paths) > 1:
                print('%s/:' % _path.rstrip('/'))
            print('\n'.join(words2lines(names)))
        except errors.DirectoryExpected:
            print('%s:' % _path.rstrip('/'))
        print()

@fs2.command()
@click.argument('paths', nargs=-1)
@click.pass_context
def cat(ctx, paths):
    fs = ctx.obj['fs']
    for path in paths:
        path = relpath(normpath(path))
        try:
            print('-------------------- cat %s --------------------' % path)
            result = fs.readbytes(path)
        except errors.FileExpected:
            print('Error: %s/ is a dir' % path, file=sys.stderr)
        else:
            print(result.decode(sys.getdefaultencoding(), 'replace'))

@fs2.command()
@click.argument('paths', nargs=-1)
@click.option('--parents', '-p', is_flag=True, help='no error if existing, make parent directories as needed')
@click.pass_context
def mkdir(ctx, paths, parents):
    """mkdir folders"""
    fs = ctx.obj['fs']
    for path in paths:
        try:
            if parents:
                fs.makedirs(path, recreate=True)
            else:
                fs.makedir(path, recreate=True)
        except errors.ResourceNotFound:
            click.echo('parent dir not exist: %s' % posixpath.dirname(path))
            break
        except errors.DirectoryExpected as e:
            click.echo('%s. Check Tip: %s' % (e, path.replace('/', '(<-aFile?) / ')))
            break

@fs2.command()
@click.argument('paths', nargs=-1)
@click.option('--recursive', '-r', is_flag=True, help='remove directories and their contents recursively')
@click.option('--force', '-f', is_flag=True, help='ignore nonexistent files and arguments, never prompt')
@click.option('--interactive', '-i', is_flag=True, help='prompt before every removal')
@click.pass_context
def rm(ctx, paths, recursive, force, interactive):
    """Be Careful to remove !!!"""
    if not force:
        click.confirm('Data is priceless. Continue [DELETE]?', abort=True, default=True)
    fs = ctx.obj['fs']
    url = ctx.obj['url']
    for path in paths:
        if interactive and not click.confirm('Ensure delete %s ?' % path, abort=True, default=True):
            return
        try:
            fs.remove(path)         # remove file
            click.echo('removed file: %s' % path)
        except errors.ResourceNotFound:
            if force:
                click.echo('[WARNING] not found and skip: %s' % path)
            else:
                click.echo('abort (unless --force) because not found: %s' % path)
        except errors.FileExpected:
            if recursive:
                fs.removetree(path) # remove dir
                click.echo('removed dir : %s' % path)
            else:
                click.echo('need --recursive/-r to rm dir %s' % path)

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

@fs2.command()
@click.argument('src', nargs=-1)
@click.argument('dst', nargs=1)
@click.option('--force', '-f', is_flag=True, help='force overwrite if existing destination file')
@click.pass_context
def mv(ctx, src, dst, force):
    """Move file from SRC to DST."""
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
            fs.move(fn, _dst, overwrite=force)
        except errors.ResourceNotFound:
            click.echo('parent dir not exists: %s' % posixpath.dirname(_dst))
            break

@fs2.command()
@click.argument('path', required=False) # 不限个数
@click.option('--max-levels', '-m', default=-1, help='Maximum number of levels to display, or -1 for no maximum')
@click.pass_context
def tree(ctx, path, max_levels):
    fs = ctx.obj['fs']
    url = ctx.obj['url']
    _path = path or '.'
    _max_levels = None if max_levels == -1 else max_levels
    click.echo(fs.tree(path=_path, max_levels=_max_levels))

if __name__ == '__main__':
    fs2()
