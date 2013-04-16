# encoding=UTF-8

# Copyright © 2010, 2011, 2012, 2013 Jakub Wilk <jwilk@jwilk.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 dated June, 1991.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

from .. import utils
from .. import image_io

import cStringIO as io

class Engine(object):

    name = None
    image_format = None
    needs_utf8_fix = False

    def __init__(self, *args, **kwargs):
        assert args == ()
        assert isinstance(self.name, str)
        assert issubclass(self.image_format, image_io.ImageFormat)
        for key, value in kwargs.iteritems():
            try:
                prop = getattr(type(self), key)
                if not isinstance(prop, utils.property):
                    raise AttributeError
            except AttributeError, ex:
                ex.args = ('%r is not a valid property for the %s engine' % (key, self.name),)
                raise
            setattr(self, key, value)

class Output(object):

    format = None

    def __init__(self, contents, format=None):
        self._contents = contents
        if format is not None:
            self.format = format
        if self.format is None:
            raise TypeError('output format is not defined')

    def __str__(self):
        return self._contents

    def save(self, prefix):
        path = '%s.%s' % (prefix, self.format)
        with open(path, 'wb') as file:
            file.write(str(self))

    def as_stringio(self):
        return io.StringIO(str(self))

# vim:ts=4 sw=4 et
