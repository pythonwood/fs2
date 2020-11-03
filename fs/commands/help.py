#!/usr/bin/env python
from .init import fs2, click, errors

@fs2.command()
@click.pass_context
def help(ctx):
    '''print this help msg.'''
    click.echo(ctx.parent.get_help()) # ctx.parent -> fs2 level

