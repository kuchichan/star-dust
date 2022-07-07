from typing import Any


class MailingMethod:
    def __init__(self, mailing_method) -> None:
        self.mailing_method = mailing_method

    def __call__(self) -> Any:
        return self.mailing_method
