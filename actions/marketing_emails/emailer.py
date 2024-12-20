from typing import Self


class Emailer:
    """Emailer.

    The careful reader will notice this class doesn't
    do anything-- it's meant to mock out an SMTP library like
    https://github.com/sendgrid/sendgrid-python
    """

    def __init__(self, _template: str) -> None:
        pass

    def build_template(self, **_kwargs: dict) -> Self:
        return self

    def send(self) -> Self:
        return self

    @property
    def sends(self) -> int:
        return 72
