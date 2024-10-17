select
    file_name,
    ARRAY_AGG(
        page_num
        order by page_num asc
    ) as gdpr_pages
from `twirldata-demo.contracts.contract_text`
where
    REGEXP_CONTAINS(page_text, r'(?i)gdpr')
group by
    file_name
