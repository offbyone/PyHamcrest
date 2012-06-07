"""
decorators.py
Matcher decorators for Hamcrest

Created by Chris Rose on 2012-06-06.
Copyright (c) 2012 Hamcrest.org. All rights reserved.
"""
import functools

from hamcrest.core.base_matcher import BaseMatcher

__author__ = "Chris Rose"
__copyright__ = "Copyright 2012 hamcrest.org"
__license__ = "BSD, see License.txt"

__all__ = ["make_matcher"]

def make_matcher(*args, **kwargs):

    def make_matcher_func(**kwargs):

        def _create_matcher_cls(fun):
            return PluggableMatcher(fun)
        return _create_matcher_cls

    if len(args) == 1 and callable(args[0]):
        return make_matcher_func(**kwargs)(args[0])

    return make_matcher_func(**kwargs)



class PluggableMatcher(BaseMatcher):

    def __init__(self, matching_function):
        self._describer = None
        self._matching_function = matching_function

    def _matches(self, obj):
        return self._matching_function(obj)

    def describe_to(self, description):
        description.append_text("matched by the function ") \
                    .append_value(self._matching_function.__name__)

    def describes_mismatch(self, func):
        self._describer = func

    def describe_mismatch(self, item, description):
        if self._describer and callable(self._describer):
            return self._describer(item, description)

        return super(PluggableMatcher, self).describe_mismatch(item, description)
