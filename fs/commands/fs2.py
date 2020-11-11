from fs import open_fs, errors
import shutil
import click
from collections import OrderedDict

def _listopener():
    from fs.opener  import registry
    openers = set(registry.get_opener(i).__class__ for i in  registry.protocols)
    for opener in openers:
        print(str(opener), 'for', ['%s://' % i for i in opener.protocols])

def _open_fs(url):
    if '://' not in url:
        url = 'file://' + url
    _fs = open_fs(url)
    setattr(_fs, 'url', url)
    return _fs


@click.group(invoke_without_command=True) #https://click.palletsprojects.com/en/7.x/commands/#group-invocation-without-command
@click.option('--listopener', '-l', is_flag=True, help='list supported file system')
@click.option('--url', '-u', multiple=True, default='.', help='filesystem url: default is "."')
@click.pass_context
def fs2(ctx, listopener, url):
    '''This script is pyfilesystem2 command line tool.

    \b
    example:
        fs2 ls .
        fs2 -u file://c:/windows ls system32
        fs2 -u zip:///tmp/a.zip ls /
        fs2 -u tar:///etc/bak.tar.gz  ls opkg config
        fs2 -u temp:// ls .
        fs2 -u s3:// ls .                                 # pip install fs-s3fs
        fs2 -u dropbox:// ls .                            # pip install fs.dropboxfs
        fs2 -u webdav://user:pass@127.0.0.1/web/dav/ ls . # pip install fs.webdavfs
        fs2 -u ssh://my.vps.com/home/ ls .                # pip install fs.sshfs
        fs2 --listopener                                  # list all support filesystem

    \b
    mutil url is supported:
        fs2 -u /tmp -u ssh://vps/tmp ls .

    '''
    # print(vars(ctx), listopener, url)
    if listopener:
        _listopener()
        ctx.exit()
    if not (ctx.args or ctx.invoked_subcommand):
        click.echo(ctx.get_help())
        ctx.exit()

    ctx.ensure_object(dict)
    # so, a for loop in group is better than for loop in subcmd
    # # ctx.obj['fss'] = OrderedDict((u, _open_fs(u)) for u in url)
    for u in url:
        ctx.obj['url'] = u
        ctx.obj['fs'] = _open_fs(u)
        subcmd = click.Group.get_command(fs2, ctx, ctx.invoked_subcommand)
        # ctx.forward(subcmd) # TypeError: ls() got an unexpected keyword argument 'url'
        # ctx.forward(fs2)    # ctx has no sub command forward
        ctx.invoke(subcmd)    # subcmd`s args is empty # click/core.py +1256
    ctx.exit()


