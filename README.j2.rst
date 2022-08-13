Fakers for SQLAlchemy
=====================

{% for badge in badges %}{{ badge.as_rst_declaration() }} {% endfor %}

{{ faker_sqlalchemy.__doc__ }}

{% for badge in badges -%}
{{ badge.as_rst_definition() }}
{% endfor %}
