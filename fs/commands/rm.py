from .init import fs2, click, errors
from fs.path import relpath, normpath

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

