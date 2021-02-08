import click
from fs import errors
from fs.path import relpath, normpath

@click.command()
@click.argument('paths', nargs=-1, required=False)
@click.option('--force', '-f', is_flag=True, help='force skip instead of aborting')
@click.pass_context
def info(ctx, paths, force):
    '''get info of resource.

    \b
    example:
        info .
        info dirA dirx/ a/b.txt

    \b
    important:
        fs,getinfo('a/b/') raise ResourceNotFound although listdir('a/b/') ok.
        only makdir ('a/b/') fix it.
    '''
    fs = ctx.obj['fs']
    url = ctx.obj['url']
    paths = paths or ['.']
    for u,f in fs.items():
        fs_info(f, paths, force)

def fs_info(fs, paths, force):
    for path in paths:
        _path = path
        path = relpath(normpath(path))
        try:
            if len(paths) > 1:
                print('%s:' % _path)
            _info = fs.getinfo(path, namespaces=('basic', 'details'))
            # print('\n'.join('%-7s %s' % (k,v) for k,v in _info.raw.items()))
            print('%s %7s bytes (modified %s)' % (
                _info.type.name[0], _info.size or 'unknown', _info.modified or 'unknown'))
        except errors.ResourceNotFound:
            if not force:
                click.confirm('%s is not exist (while resource under it may be exist). Skip?' % _path,
                              abort=True, default=True)
        print()

