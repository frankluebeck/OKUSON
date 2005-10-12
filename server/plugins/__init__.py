# -*- coding: ISO-8859-1 -*-
#
#   Extension framework for Okuson
#
#   Copyright (C) 2005  Ingo Klöcker <ingo.kloecker@mathA.rwth-aachen.de>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import os, sys

from fmTools import Utils

Utils.Error( 'Loading extensions...', prefix='Info: ' )

import plugins

pluginNames = os.listdir( os.path.join( plugins.__path__[0] ) )
for pluginName in pluginNames:
    name, ext = os.path.splitext( pluginName )
    if name != '__init__' and ext == '.py':
        module = None
        try:
            module = __import__( plugins.__name__ + '.' + name )
        except ImportError:
            Utils.Error( 'Importing plugin ' + name + ' failed' )
            # if the ImportError happened in the module being imported,
            # this is a failure that should be handed to our caller.
            # count stack frames to tell the difference.
            import traceback
            exc_info = sys.exc_info()
            if len( traceback.extract_tb( exc_info[2] ) ) > 1:
                try:
                    # Clean up garbage left in sys.modules.
                    del sys.modules[name]
                except KeyError:
                    # Python 2.4 has fixed this.  Yay!
                    pass
                raise exc_info[0], exc_info[1], exc_info[2]

__all__ = []
