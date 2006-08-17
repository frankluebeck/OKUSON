# -*- coding: ISO-8859-1 -*-
#
#   Extension framework for Okuson
#
#   Copyright (C) 2005,2006  Ingo Klöcker <ingo.kloecker@mathA.rwth-aachen.de>
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

'''Framework for adding extensions to Okuson

   If you want to add an extension (a plugin) to Okuson then all you have to
   do is add a new file to the "plugins" folder containing a subclass of
   the below OkusonExtension implementing all necessary methods, e. g.

        import Plugins

        class NewExtension( Plugins.OkusonExtension ):
            def __init__( self, options = {} ):
            [...]

   Additionally, this file has to call Plugins.register to register the
   extension with Okuson, e. g.

        Plugins.register( 'ExtensionName',
                          'Category',
                          'Short description of the extension',
                          'Long description of the extension.',
                          'Author of the extension',
                          'Copyright of the extension',
                          'Copyright year',
                          ClassNameOfTheExtension )
'''

import string, re

from fmTools import Utils

HTML = 0
File = 1

# Credential values
Anonymous = 0
Student = 1
Tutor = 2
Admin = 3

_registered_extensions_ = {}

class error:
    pass

def register( extensionName, category, shortDesc, longDesc, author, copyright,
              date, extensionClass ):
    '''Call this to register your extension.'''

    # perform some sanity checks on the data
    def letterCheck( str ):
        allowed = string.letters + string.digits + '_'
        for ch in str:
            if not ch in allowed:
                    return 0
        else:
            return 1

    if not letterCheck( extensionName ):
        raise error, 'extension name contains illegal characters'

    # check whether the extension is a subclass of OkusonSimpleExtension
    try:
        issubclass( extensionClass, OkusonSimpleExtension )
    except TypeError:
        return 1
    # check whether the extension is an OkusonExtension
    try:
        isSimpleExtension = not issubclass( extensionClass, OkusonExtension )
    except TypeError:
        isSimpleExtension = True

    _registered_extensions_[ extensionName ] = \
        ( category, shortDesc, longDesc, author, copyright, date,
          isSimpleExtension, extensionClass )

def dumpExtensions():
    '''Writes the list of registered extensions to stderr.'''
    Utils.Error( 'List of registered extensions:', prefix='Info: ' )
    for extensionName in _registered_extensions_.keys():
        ( category, shortDesc, longDesc, author, copyright, date,
          isSimpleExtension, extensionClass ) = _registered_extensions_[extensionName]
        p = extensionClass()
        Utils.Error( p.name(), prefix='- ' )

def listExtensions( handler, which = Anonymous ):
    '''Creates HTML code containing the form code of all registered (non-simple)
       extensions with necessary credentials @p which.'''
    # sort all extensions by category
    categories = {}
    for extensionName in _registered_extensions_.keys():
        ( category, shortDesc, longDesc, author, copyright, date, 
          isSimpleExtension, extensionClass ) = _registered_extensions_[extensionName]
        # skip simple extensions
        if isSimpleExtension:
            continue
        p = extensionClass()
        if which == p.necessaryCredentials():
            if not categories.has_key( category ):
                categories[category] = []
            categories[category].append( extensionName )
    if len( categories ) == 0: # no matching extensions found
        return '<p><em>No extensions found.</em></p>\n'
    toc = []
    body = ''
    catList = categories.keys()
    catList.sort()
    for c in catList:
        # Create a suitable HTML anchor from the category name by removing all
        # characters which are no ASCII letter
        anchor = re.sub( '[^A-Za-z]', '', c )
        toc.append( '<a href="#' + anchor + '">' + c + '</a>' )
        body += ( '<hr />\n\n'
                  '<h4 id="' + anchor + '">' + c + '</h4>\n' )
        extList = categories[c]
        extList.sort()
        for extensionName in extList:
            ( category, shortDesc, longDesc, author, copyright, date, 
              isSimpleExtension, extensionClass ) = _registered_extensions_[extensionName]
            body += extensionForm( extensionName, handler )
    return ( '<ul>\n<li>' + str('</li>\n<li>').join( toc ) + '</li>\n</ul>\n' +
             body )

def extensionExists( extensionName ):
    '''Returns True, if an extension with the given name exists,
       and returns False otherwise.'''
    return _registered_extensions_.has_key( extensionName )

def necessaryCredentials( extensionName, options ):
    '''Returns the credentials that are necessary for using the given extension
       or None if there is no extension with the given name. Possible return
       values are Anonymous, Student, Tutor, Admin.'''
    if not extensionExists( extensionName ):
        return None
    ( category, shortDesc, longDesc, author, copyright, date,
      isSimpleExtension, extensionClass ) = _registered_extensions_[extensionName]
    if isSimpleExtension:
        return None
    p = extensionClass()
    return p.necessaryCredentials()

def extensionForm( extensionName, handler ):
    '''Returns the form code of the extension with the given name.'''
    try:
        ( category, shortDesc, longDesc, author, copyright, date, 
          isSimpleExtension, extensionClass ) = _registered_extensions_[extensionName]
    except:
        return ''
    if isSimpleExtension:
        return ''
    s = ''
    p = extensionClass()
    if p.necessaryCredentials() == Admin:
        s = ( '<form action="/AdminExtension" method="post"><p>\n'
              '<input type="hidden" name="extension" value="' + 
              extensionName + '" />\n'
              '<input type="submit" name="Action" value="Go" />\n'
              '' + handler.AdminPasswdField() + ''
              ' ' + p.formCode() + '\n'
              '</p></form>\n' )
    else:
        s = ( '<form action="/Extension" method="post"><p>\n'
              '<input type="hidden" name="extension" value="' + 
              extensionName + '" />\n'
              '<input type="submit" name="Action" value="Go" />\n'
              ' ' + p.formCode() + '\n'
              '</p></form>\n' )
    return s

def returnType( extensionName, options ):
    '''Returns the return type of the extension with the given name for the
       given options. This is either HTML or File.'''
    try:
        ( category, shortDesc, longDesc, author, copyright, date, 
          isSimpleExtension, extensionClass ) = _registered_extensions_[extensionName]
    except:
        return 'Error: Unknown Extension'
    if isSimpleExtension:
        return 'Error: Unknown Extension'
    p = extensionClass( options )
    return p.returnType()

def extensionTitle( extensionName, options ):
    '''Returns the (HTML) title of the extension with the given name.'''
    try:
        ( category, shortDesc, longDesc, author, copyright, date, 
          isSimpleExtension, extensionClass ) = _registered_extensions_[extensionName]
    except:
        return 'Error: Unknown Extension'
    if isSimpleExtension:
        return 'Error: Unknown Extension'
    p = extensionClass( options )
    return p.title()

def extensionCSS( extensionName, options ):
    '''Returns optional CSS for the extension with the given name.'''
    try:
        ( category, shortDesc, longDesc, author, copyright, date, 
          isSimpleExtension, extensionClass ) = _registered_extensions_[extensionName]
    except:
        return 'Error: Unknown Extension'
    p = extensionClass( options )
    return p.cssCode()

def extensionCode( extensionName, options ):
    '''Returns the HTML code for the extension with the given name for the
       given options.'''
    try:
        ( category, shortDesc, longDesc, author, copyright, date, 
          isSimpleExtension, extensionClass ) = _registered_extensions_[extensionName]
    except:
        return '<p>Error: Unknown extension</p>'
    p = extensionClass( options )
    return p.htmlCode()

def createHeadAndBody( extensionName, options ):
    '''Returns a pair consisting of HTTP header and body for the extension with
       the given name for the given options.'''
    try:
        ( category, shortDesc, longDesc, author, copyright, date, 
          isSimpleExtension, extensionClass ) = _registered_extensions_[extensionName]
    except:
        return '<p>Error: Unknown extension</p>'
    if isSimpleExtension:
        return '<p>Error: Unknown extension</p>'
    p = extensionClass( options )
    return p.headAndBody()


class OkusonSimpleExtension:
    '''This is the base class for simple Okuson extensions. Simple Okuson
       extensions are used to replace <Extension name="foo" /> tags with some HTML
       code.'''
    def __init__( self, options = {} ):
        pass
    def name( self ):
        '''Return the name of the extension.'''
        raise error, 'Implementation of "name" missing.'
    def cssCode( self ):
        '''The cssCode is inserted in place of a <ExtensionCSS extension="foo" />
           tag.
           This method should return any CSS definitions you need for the
           extension's HTML code.'''
        raise error, 'Implementation of "cssCode" missing.'
    def htmlCode( self ):
        '''The htmlCode is inserted in place of a <ExtensionCode extension="foo" />
           tag.
           This method should return the extension's HTML code.'''
        raise error, 'Implementation of "htmlCode" missing.'

class OkusonExtension( OkusonSimpleExtension ):
    '''This is the base class for normal Okuson extensions.'''
    def __init__( self, options = {} ):
        '''Initialize the extension with the options from the HTML form.'''
        raise error, 'Implementation of "__init__" missing.'
    def necessaryCredentials( self ):
        '''Returns the credentials that are necessary for using this
           extension. Possible values are:
           Anonymous - Extension for everybody.
           Student   - Extension for registered students.
           Tutor     - Extension for tutors.
           Admin     - Extension for administrators.'''
        raise error, 'Implementation of "necessaryCredentials" missing.'
    def returnType( self ):
        '''Return Plugins.HTML if this extension returns HTML code. In this
           case you also have to implement title(), cssCode() and htmlCode().
           If this extension creates a file (e.g. a text file or a PDF) then
           return Plugins.File. In this case you also have to implement
           headAndBody().'''
        raise error, 'Implementation of "returnType" missing.'
    def title( self ):
        '''The title will be shown as title of the HTML page that is created
           for this extension.'''
        raise error, 'Implementation of "title" missing.'
    def formCode( self ):
        '''The formCode is inserted into a <form> element on the page with
           the list of extensions and on pages on which this extension is
           requested by a <ExtensionForm extension="foo" /> tag.
           This method should return a short description of the extension
           and, optionally, form elements to request options/data from the
           user.'''
        raise error, 'Implementation of "formCode" missing.'
    def cssCode( self ):
        '''The cssCode is inserted into a <style> element in the HTML header
           of the webpage for this extension or in place of a
           <ExtensionCSS extension="foo" /> tag.
           This method should return any CSS definitions you need for the
           extension's HTML code.'''
        raise error, 'Implementation of "cssCode" missing.'
    def htmlCode( self ):
        '''The htmlCode is inserted into the body of the webpage for this
           extension or in place of a <ExtensionCode extension="foo" /> tag.
           This method should return the extension's HTML code.'''
        raise error, 'Implementation of "htmlCode" missing.'
    def headAndBody( self ):
        '''This method should return a pair consisting of the HTTP header and
           the data this extension creates.'''
        raise error, 'Implementation of "headAndBody" missing.'
