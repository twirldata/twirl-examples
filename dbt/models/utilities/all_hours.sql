select hour
from UNNEST(
    GENERATE_TIMESTAMP_ARRAY(
        TIMESTAMP('2020-01-01 00:00:00'),
        TIMESTAMP_ADD(CURRENT_TIMESTAMP(), interval 365 day),
        interval 1 hour
    )
) as hour
