{% extends "mail_templated/base.tpl" %}
{% block subject %}
Hello {{name}}
{% endblock %}

{% block html %}
Your verify code is <strong>66636</strong>
{% endblock %}