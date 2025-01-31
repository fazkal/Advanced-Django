{% extends "mail_templated/base.tpl" %}
{% block subject %}
Account Activation and Verification
{% endblock %}

{% block html %}
<strong>{{token}}</strong>
{% endblock %}