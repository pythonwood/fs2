from .init import fs2, click, errors
from fs.path import relpath, normpath

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

