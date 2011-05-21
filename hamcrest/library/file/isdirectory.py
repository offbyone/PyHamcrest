import os

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.string_description import StringDescription

__author__ = "Chris Rose"
__copyright__ = "Copyright 2011 hamcrest.org"
__license__ = "BSD, see License.txt"

class IsDirectoryPath(BaseMatcher):

    def _matches(self, o):
        if o is None:
            return False

        if not os.path.exists(o):
            return False

        if not os.path.isdir(o):
            return False

        return True

    def describe_to(self, description):
        description.append_text('a path that is a directory')

    def describe_mismatch(self, item, mismatch_description):
        if item is None:
            mismatch_description.append_text('was None')
            return

        if not os.path.exists(item):
            mismatch_description.append_text('did not exist')
            return

        if not os.path.isdir(item):
            mismatch_description.append_text('was not a directory')
            return


def is_directory():
    """Matches paths that refer to a directory
    """
    return IsDirectoryPath()
