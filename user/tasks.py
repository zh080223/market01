from django.core import mail

from market01.celery import app


@app.task
def send_test_email_celery(recipient, subject, message):
    print('celery')
    mail.send_mail(
        subject=subject,
        message=message,
        from_email='402306174@qq.com',
        recipient_list=[recipient],
    )
