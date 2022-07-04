from typing import Any, Dict, Optional, Tuple, Union

import emails
from emails.template import JinjaTemplate as T

from star_dust.core.config import settings


def email_send(
    mail_to: Tuple[str, ...],
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
        to=mail_to,
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
