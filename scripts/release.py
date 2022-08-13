import os
import shutil
import subprocess
import sys

BASEDIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__),
    )
)
PYENV_HOME = os.environ.get("PYENV_HOME", None)
PYTHON_EXECUTABLES = [
    "python",
    "python3.7",
    "python3.8",
    "python3.9",
    "python3.10",
    "make",
    "tox",
    "flit",
]


def validate_executables():
    errors = []
    for executable in PYTHON_EXECUTABLES:
        if shutil.which(executable) is None:
            errors.append(f"No executable named {executable} found on path.")
    if errors:
        print("* " + "\n* ".join(errors))
        sys.exit(1)


def setup_pyenv():
    global PYENV_HOME

    if PYENV_HOME is None:
        user_home = os.environ.get("HOME", None)
        if user_home:
            if os.path.exists(
                os.path.join(user_home, ".pyenv")
            ):
                PYENV_HOME = os.path.join(user_home, ".pyenv")

    if PYENV_HOME is not None:
        shims_path = os.path.join(
            PYENV_HOME,
            "shims",
        )
        if os.path.isdir(shims_path) and shims_path not in os.environ.get("PATH", ""):
            os.environ["PATH"] = f"{shims_path}{os.pathsep}{os.environ['PATH']}"


def main():
    setup_pyenv()

    validate_executables()

    subprocess.run(
        [sys.executable, "scripts/update_readme.py"],
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
