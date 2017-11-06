BADGE_URL = 'https://img.shields.io/badge/{0}-{1}-{2}.svg?style=flat'
BADGE_NAME = 'TRSV'


def _badge_escape(input_string):
    return input_string.replace('-', '--')


def passing_badge():
    status_text = 'passing'
    status_color = 'brightgreen'
    return BADGE_URL.format(_badge_escape(BADGE_NAME), _badge_escape(status_text), status_color)


def warning_badge():
    status_text = 'warning'
    status_color = 'orange'
    return BADGE_URL.format(_badge_escape(BADGE_NAME), _badge_escape(status_text), status_color)


def failing_badge():
    status_text = 'failed'
    status_color = 'red'
    return BADGE_URL.format(_badge_escape(BADGE_NAME), _badge_escape(status_text), status_color)


def error_badge():
    status_text = 'error'
    status_color = 'red'
    return BADGE_URL.format(_badge_escape(BADGE_NAME), _badge_escape(status_text), status_color)

