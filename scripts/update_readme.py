"""Updates the `README.rst` at the root of the repository with the latest documentation."""
import os
import sys

import jinja2


_PYPI_URL = "https://pypi.org/project/faker_sqlalchemy/"
_PYPI_SHIELD = "https://img.shields.io/pypi/v/faker_sqlalchemy"
_PYPI_LABEL = "PyPI"

_VERSIONS_SHIELD = "https://img.shields.io/pypi/pyversions/faker_sqlalchemy.svg"
_VERSIONS_LABEL = "Supported Python versions"

_RTFM_URL = "https://faker-sqlalchemy.readthedocs.io/en/latest/?badge=latest"
_RTFM_SHIELD = "https://readthedocs.org/projects/faker-sqlalchemy/badge/?version=latest"
_RTFM_LABEL = "Documentation"

_STAT_URL = "https://pepy.tech/project/faker_sqlalchemy/"
_STAT_SHIELD = "https://pepy.tech/badge/faker_sqlalchemy/month"
_STAT_LABEL = "Downloads"


def _render_badge(label, badge, url):
    return f"[![{label}]({badge})]({url})"


def main():
    base_dir = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
    sys.path.insert(0, base_dir)

    import faker_sqlalchemy

    badges = [
        _render_badge(_PYPI_LABEL, _PYPI_SHIELD, _PYPI_URL),
        _render_badge(_VERSIONS_LABEL, _VERSIONS_SHIELD, _PYPI_URL),
        _render_badge(_RTFM_LABEL, _RTFM_SHIELD, _RTFM_URL),
        # _render_badge(_STAT_LABEL, _STAT_SHIELD, _STAT_URL),
    ]

    template_path = os.path.join(base_dir, "README.j2.rst")
    with open(template_path) as f:
        content = f.read()

    template = jinja2.Template(content)
    result = template.render(
        **globals(),
        **locals(),
    )

    readme_path = os.path.join(base_dir, "README.rst")
    with open(readme_path, "w") as f:
        f.write(result)


if __name__ == '__main__':
    main()
