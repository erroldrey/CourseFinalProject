# coding: ascii
import smtplib


def send_email(subject, to_addr, body_text):
    """
    Send an email
    """

    BODY = "\r\n".join((
        "From: %s" % '...@...',
        "To: %s" % to_addr,
        "Subject: %s" % subject,
        "",
        body_text
    ))

    server = smtplib.SMTP('...', 587)
    server.login('?????', '??????')
    server.sendmail('...@...', [to_addr], BODY)
    server.quit()
