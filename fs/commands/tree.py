from .init import fs2, click, errors
from fs.path import relpath, normpath

@fs2.command()
@click.argument('path', required=False) # 不限个数
@click.option('--max-levels', '-m', default=-1, help='Maximum number of levels to display, or -1 for no maximum')
@click.pass_context
def tree(ctx, path, max_levels):
    '''list files and dirs as tree view.
    example:
        tree .
    '''
    fs = ctx.obj['fs']
    _path = path or '.'
    _max_levels = None if max_levels == -1 else max_levels
    click.echo(fs.tree(path=_path, max_levels=_max_levels))
