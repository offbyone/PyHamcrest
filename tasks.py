#!/usr/bin/env invoke
import sys
import subprocess

from invoke import task, Collection

# from invocations.packaging import release


def is_dirty(path="."):
    """
    Check whether the local repo or *path* contains uncommited changes.
    """
    out = subprocess.check_output(f"git status --porcelain {path}", shell=True)

    return len(out) != 0


@task
def release(c, version):
    if not version[0] in "0123456789":
        # we have an accidental flag
        print(f"{version} is not a version")
        sys.exit(1)

    c.run("rm -fv dist/*", warn=True, hide=True)
    with open("src/hamcrest/__init__.py") as fh:
        ver_lines = list(fh)

    index, ver_line = [(i, v) for i, v in enumerate(ver_lines) if v.startswith("__version__")][0]
    ver_lines[index] = f'__version__ = "{version}"\n'

    with open("src/hamcrest/__init__.py", mode="w") as fh:
        fh.writelines(ver_lines)

    c.run("git add src/hamcrest/__init__.py")

    c.run("towncrier --yes")
    c.run(f"git commit -m 'Cutting V{version}'")
    c.run(f"git tag V{version}")
    c.run("python3 setup.py sdist bdist_wheel")
    c.run("twine check dist/*")
    c.run("twine upload dist/*")


ns = Collection(
    release,
)
