from collections.abc import Callable
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import emails
from emails.template import JinjaTemplate as T

from star_dust.core.config import settings
from star_dust.models.user import User

SendMailSignature = Callable[
    [
        Tuple[Optional[str], ...],
        Union[str, bytes],
        Union[str, bytes],
        Optional[Dict[str, Any]],
    ],
    None,
]


def send_email(
    email_to: Tuple[str, ...],
    subject: Union[str, bytes],
    body: Union[str, bytes],
    environment: Optional[Dict[str, Any]] = None,
) -> None:
    environment = environment if environment is not None else {}
    message = emails.html(
        subject=T(subject),
        html=T(body),
        mail_from=(settings.sender_email_name, settings.sender_email_address),
    )

    response = message.send(
        to=email_to,
        render=environment,
        smtp={
            "host": settings.smtp_host,
            "port": settings.smtp_port,
            "user": settings.smtp_user,
            "tls": settings.smtp_tls,
            "password": settings.smtp_password,
        },
    )
    return response


def send_user_registration_link(
    user: User, registration_link: str, mailing_method: SendMailSignature
):
    with open(
        Path(settings.email_templates_dir) / "registration.html", encoding="utf-8"
    ) as f:
        template = f.read()

    mailing_method(
        (user.nickname, user.email),
        "Welcome to Star - Dust!",
        template,
        {"nickname": user.nickname, "registration_link": registration_link},
    )
