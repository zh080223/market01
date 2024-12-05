from django.core import mail


def send_test_email(recipient, subject, message):
    mail.send_mail(
        subject=subject,
        message=message,
        from_email='402306174@qq.com',
        recipient_list=[recipient],
    )
