#! /usr/bin/env python3
# coding: utf8

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
def fscmd(ctx, listopener, url):
    '''This script is pyfilesystem2 command line tool.

    \b
    example:
        fscmd ls .
        fscmd -u file://c:/windows ls system32
        fscmd -u zip:///tmp/a.zip ls /
        fscmd -u tar:///etc/bak.tar.gz  ls opkg config
        fscmd -u temp:// ls .
        fscmd -u s3:// ls .                                 # pip install fs-s3fs
        fscmd -u dropbox:// ls .                            # pip install fs.dropboxfs
        fscmd -u webdav://user:pass@127.0.0.1/web/dav/ ls . # pip install fs.webdavfs
        fscmd -u ssh://my.vps.com/home/ ls .                # pip install fs.sshfs
        fscmd --listopener                                  # list all support filesystem

    \b
    mutil url is supported:
        fscmd -u /tmp -u ssh://vps/tmp ls .

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
    # but not subcmd content pass then no way. see click/core.py +1256
    ctx.obj['fs'] = OrderedDict((u, _open_fs(u)) for u in url)
    ctx.obj['url'] = '\n'.join(url)
    # for u in url:
    #     ctx.obj['url'] = u
    #     ctx.obj['fs'] = _open_fs(u)
    #     subcmd = click.Group.get_command(fscmd, ctx, ctx.invoked_subcommand)
    #     # ctx.forward(subcmd) # TypeError: ls() got an unexpected keyword argument 'url'
    #     # ctx.forward(fscmd)    # ctx has no sub command forward
    #     # ctx.invoke(subcmd)  # subcmd`s args is empty # click/core.py +1256


if __name__ == '__main__':
    fscmd()
