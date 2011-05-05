from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.core.anyof import any_of
from hamcrest.core.core.allof import all_of
from hamcrest.core.helpers.hasmethod import hasmethod
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.library.collection import has_items, only_contains

__author__ = "Chris Rose"
__copyright__ = "Copyright 2011 hamcrest.org"
__license__ = "BSD, see License.txt"


class IsSequenceExactlyContaining(BaseMatcher):
    """Matches sequences that exactly contain elements satisfying a given
    matcher.

    This matcher will only match an empty sequence if no matchers are provided

    """

    def __init__(self, matchers):
        self.matchers = matchers

    def _matches(self, sequence):
        try:
            if len(self.matchers) == 0 and len(sequence) == 0:
                return True
        except TypeError:
            # not a sequence
            return False

        any_matcher = self._match_any()
        for item in sequence:
            if not any_matcher.matches(item):
                return False

        has_all = self._match_all()
        if not has_all.matches(sequence):
            return False

        return True

        if len(sequence) == 0:
            return False
        for item in sequence:
            if not self.matcher.matches(item):
                return False
        return True

    def _match_any(self):
        return any_of(*self.matchers)

    def _match_all(self):
        return has_items(*self.matchers)

    def describe_to(self, description):
        description.append_text('a sequence consisting of all items matching ')    \
                    .append_description_of(self._match_any())


def contains_exactly(*items):
    """Matches sequences that only contain elements satisfying any of a
    list of items, and for which every item is represented.  This is the
    equivalent of all_of(has_items(), only_contains())

    For example, ``[3,1,2]`` would satisfy ``contains_exactly(less_than(3), 3)``.

    If an item is not a matcher, it is equivalent to ``equal_to(item)``, so the
    list in the example above would also satisfy ``contains_exactly(1,2,3)``.

    """
    matchers = []
    for item in items:
        matchers.append(wrap_matcher(item))
    return IsSequenceExactlyContaining(matchers)
