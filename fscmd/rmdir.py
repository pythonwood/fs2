import click
from fs import errors
from fs.path import relpath, normpath

@click.command()
@click.argument('paths', nargs=-1, required=False)
@click.option('--force', '-f', is_flag=True, help='force skip instead of aborting')
@click.pass_context
def rmdir(ctx, paths, force):
    '''get info of resource.

    \b
    example:
        rmdir a/dir/to/del
        rmdir dirA/ dirB/emptydir a/b/c

    '''
    fs = ctx.obj['fs']
    url = ctx.obj['url']
    paths = paths or ['.']
    for u,f in fs.items():
        fs_rmdir(f, paths, force)

def fs_rmdir(fs, paths, force):
    for path in paths:
        _path = path
        path = relpath(normpath(path))
        try:
            _info = fs.removedir(path)
        except errors.FSError as e:
            if not force:
                click.confirm('%s. Skip?' % e, abort=True, default=True)

