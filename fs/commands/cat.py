import sys
from .init import fs2, click, errors
from fs.path import relpath, normpath

@fs2.command()
@click.argument('paths', nargs=-1)
@click.pass_context
def cat(ctx, paths):
    fs = ctx.obj['fs']
    for path in paths:
        path = relpath(normpath(path))
        try:
            result = fs.readbytes(path)
        except errors.FileExpected:
            click.echo('Error: %s/ is a dir' % path)
        else:
            click.echo(result.decode(sys.getdefaultencoding(), 'replace'))

