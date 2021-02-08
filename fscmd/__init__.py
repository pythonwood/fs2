#!/usr/bin/env python

from .fscmd   import fscmd
from .ls    import ls
from .cat   import cat
from .mkdir import mkdir
from .rmdir import rmdir
from .tree  import tree
from .cp    import cp
from .mv    import mv
from .rm    import rm
from .dl    import dl
from .up    import up
from .info  import info

fscmd.add_command(ls   )
fscmd.add_command(cat  )
fscmd.add_command(mkdir)
fscmd.add_command(rmdir)
fscmd.add_command(tree )
fscmd.add_command(cp   )
fscmd.add_command(mv   )
fscmd.add_command(rm   )
fscmd.add_command(dl   )
fscmd.add_command(up   )
fscmd.add_command(info )

__all__ = ["fscmd"]
