from django.core.mail import send_mail


def send_request_success(email):
    send(
        'Привет!\nМы одобрили Ваше заявление!',
        email,
    )


def send(text, email):
    send_mail(
        'KEU',
        text,
        'fromsitest@yandex.com',
        [email],
        fail_silently=False,
    )
