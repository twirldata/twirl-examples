select date
from UNNEST(
    GENERATE_DATE_ARRAY(
        DATE('2020-01-01'),
        DATE_ADD(CURRENT_DATE(), interval 365 day),
        interval 1 day
    )
) as date
