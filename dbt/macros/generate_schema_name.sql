{% macro generate_schema_name(custom_schema_name, node) -%}
    {{ dbt_twirl.twirl_schema_name(custom_schema_name, node) }}
{%- endmacro %}
