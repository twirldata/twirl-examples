{% macro generate_alias_name(custom_alias_name=none, node=none) -%}
    {{ dbt_twirl.twirl_alias_name(custom_alias_name, node) }}
{%- endmacro %}
