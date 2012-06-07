from hamcrest.core.string_description import StringDescription

import unittest
import logging

log = logging.getLogger(__name__)

from hamcrest.core.matcher import Matcher
from hamcrest_unit_test.matcher_test import MatcherTest
from hamcrest import assert_that, is_, equal_to

__author__ = "Chris Rose"
__copyright__ = "Copyright 2012 hamcrest.org"
__license__ = "BSD, see License.txt"

from hamcrest import make_matcher

class DecoratorTest(MatcherTest):

    def test_that_decorator_creates_matcher(self):

        @make_matcher
        def dummy_matcher(obj):
            pass

        assert_that(dummy_matcher, is_(Matcher))

    def test_that_decorator_creates_matcher(self):

        @make_matcher
        def dummy_matcher(obj):
            pass

        self.assert_description("matched by the function 'dummy_matcher'",
                                dummy_matcher)

    def test_that_decorator_matcher_calls_wrapped_function(self):

        target_obj = object()
        other_obj = object()

        @make_matcher
        def dummy_matcher(obj):
            return obj is target_obj

        self.assert_matches('the dummy matcher matches the target', dummy_matcher, target_obj)
        self.assert_does_not_match('the dummy matcher matches the target', dummy_matcher, other_obj)

    def test_that_successful_match_does_not_generate_mismatch_description(self):
        calls = []
        @make_matcher
        def dummy_matcher(obj):
            return True

        @dummy_matcher.describes_mismatch
        def describer(obj, description):
            calls.append('describer')

        self.assert_no_mismatch_description(dummy_matcher, None)

    def test_default_description(self):
        @make_matcher
        def dummy_matcher(obj):
            return False

        self.assert_describe_mismatch('was <None>', dummy_matcher, None)

    def test_set_description_function(self):

        @make_matcher
        def dummy_matcher(obj):
            return False

        @dummy_matcher.describes_mismatch
        def describer(obj, description):
            description.append_text('DESCRIBER')

        self.assert_describe_mismatch('DESCRIBER', dummy_matcher, object())
