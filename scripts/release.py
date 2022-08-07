import os
import subprocess

BASEDIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__),
    )
)


def main():
    subprocess.run(
        ["python", "scripts/update_readme.py"],
        cwd=BASEDIR,
        check=True,
    )
    subprocess.run(
        ["make", "html"],
        cwd=os.path.join(BASEDIR, "docs"),
        check=True,
    )
    subprocess.run(
        ["tox", "--skip-missing-interpreters=false"],
        cwd=BASEDIR,
        check=True,
    )
    subprocess.run(
        ["flit", "build"],
        cwd=BASEDIR,
        check=True
    )


if __name__ == '__main__':
    main()
