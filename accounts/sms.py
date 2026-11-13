from django.conf import settings


def send_sms(phone, text):
    """Send an SMS. Returns True if it was sent.

    In 'console' mode (free) the message is printed in the server terminal.
    A real SMS gateway can be connected here later.
    """
    mode = getattr(settings, 'SMS_MODE', 'console')
    if mode == 'console':
        print('\n[SMS to %s] %s\n' % (phone, text))
        return True
    return False