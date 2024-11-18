import pandas as pd
import requests

from .emailer import Emailer


def job(input_tables: dict[str, pd.DataFrame]) -> None:
    """Mock marketing email sender.

    Show how you could use SMTP from Python to send
    data informed marketing emails to specific users
    """
    users = input_tables["dim_customers"]
    products = input_tables["dim_products"]
    product_perf = input_tables["fct_product_performance"]

    ranked = product_perf.sort_values("daily_views")
    tier_one = products[products.customer_tier == 1].product_id

    top_products = ranked[ranked.product_id.isin(tier_one)].product_id.head(3)

    res = requests.get("https://mailchimp.com/developer/marketing/api/templates/", timeout=10)
    res.raise_for_status()

    emailer = Emailer(res.text)
    for email in users.email:
        emailer.build_template(
            email=email,
            top_products=top_products,
        ).send()

    # No return value as this job performs an action, and should not write to the table
