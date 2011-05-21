from __future__ import absolute_import

import re

from hamcrest.core.helpers.hasmethod import hasmethod

def _wrap_string_literal(o):
    from ._ast import Literal
    return Literal(str(o))

def to_pattern(o):
    if hasmethod(o, 'build_regexp'):
        return o
    return _wrap_string_literal(o)

def quote(value):
    return re.escape(str(value))


class BasePatternMatcher(object):

    def build_regexp(self, builder, groups):
        self._build_regexp(builder, groups)
