import click
from fs import errors
from fs.path import relpath, normpath
import posixpath

@click.command()
@click.argument('paths', nargs=-1)
@click.option('--parents', '-p', is_flag=True, help='no error if existing, make parent directories as needed')
@click.option('--force', '-f', is_flag=True, help='force skip if instead of aborting')
@click.pass_context
def mkdir(ctx, paths, parents, force):
    """create directory.

    \b
    example:
        mkdir dir1 dir2
        mkdir -p dir1/sub/dir dir2/
    """
    fs = ctx.obj['fs']
    for path in paths:
        try:
            if parents:
                fs.makedirs(path, recreate=True)
            else:
                fs.makedir(path, recreate=False)
        except errors.ResourceNotFound:
            if not force:
                click.confirm('parent dir %s not exist. Skip?' % posixpath.dirname(path), abort=True, default=True)
        except errors.DirectoryExpected as e:
            if not force:
                click.confirm('%s file path found %s. Skip?' % (e, path.replace('/', '(<-aFile?) / ')), abort=True, default=True)
        except errors.DirectoryExists as e:
            if not force:
                click.confirm('dir %s already exits. Skip?' % path, abort=True, default=True)

