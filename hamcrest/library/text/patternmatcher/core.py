__author__ = "Chris Rose"
__copyright__ = "Copyright 2011 hamcrest.org"
__license__ = "BSD, see License.txt"

import re

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.string_description import StringDescription
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

from ._ast import GroupNamespace

class PatternMatchException(Exception):
    pass

class PatternMatcher(BaseMatcher):

    def __init__(self, pattern):
        self.pattern = pattern
        self.groups = GroupNamespace()
        super(PatternMatcher, self).__init__()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        try:
            return self.regexp
        except (TypeError, ValueError, AttributeError):
            return str(self.pattern)

    def matches(self, item, mismatch_description=None):
        matches = (self.compiled_pattern.match(item) is not None)
        if not matches:
            if mismatch_description is None:
                mismatch_description = StringDescription()

            self.describe_mismatch(item, mismatch_description)

        return matches

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append_text(' did not match the pattern ') \
                            .append_text(self.regexp)

    @property
    def compiled_pattern(self):
        if hasattr(self, '_compiled_pattern') and self._compiled_pattern is not None:
            return self._compiled_pattern

        self._compiled_pattern = re.compile(self.regexp + r'\Z', re.DEBUG)
        return self._compiled_pattern

    @property
    def regexp(self):
        if hasattr(self, '_regexp') and self._regexp is not None:
            return self._regexp

        self._regexp = self.build_regexp()
        return self._regexp


    def build_regexp(self):
        builder = []
        self.pattern.build_regexp(builder, self.groups)
        return ''.join(str(b) for b in builder)


def matches_pattern(pattern):
    return PatternMatcher(pattern)
