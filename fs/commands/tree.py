from .init import fs2, click, errors
from fs.path import relpath, normpath

@fs2.command()
@click.argument('paths', nargs=-1, required=False)
@click.option('--max-levels', '-m', default=-1, help='Maximum number of levels to display, or -1 for no maximum')
@click.pass_context
def tree(ctx, paths, max_levels):
    '''list files and dirs as tree view.
    example:
        tree .
        tree dirA dirB fileC
    '''
    fs = ctx.obj['fs']
    paths = paths or ['.']
    for _path in paths:
        click.echo('%s:' % _path)
        _max_levels = None if max_levels == -1 else max_levels
        click.echo(fs.tree(path=_path, max_levels=_max_levels))
