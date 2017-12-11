BADGE_URL = 'https://img.shields.io/badge/{0}-{1}-{2}.svg?style=flat'
BADGE_NAME = 'TRSV'


def _badge_escape(input_string):
    """

    :param input_string: a string that may need to be escaped to construct badge URL
    :return: escaped string compatible with the badge URL
    """
    return input_string.replace('-', '--')


def passing_badge():
    """

    :return: A badge denoting that the validation has passed
    """
    status_text = 'passing'
    status_color = 'brightgreen'
    return BADGE_URL.format(
        _badge_escape(BADGE_NAME),
        _badge_escape(status_text),
        status_color)


def warning_badge():
    """

    :return: A badge denoting that the validation does not contain any errors or failures, but some skipped endpoints
    """
    status_text = 'warning'
    status_color = 'orange'
    return BADGE_URL.format(
        _badge_escape(BADGE_NAME),
        _badge_escape(status_text),
        status_color)


def failing_badge():
    """

    :return: A badge denoting that the validation has failed
    """
    status_text = 'failed'
    status_color = 'red'
    return BADGE_URL.format(
        _badge_escape(BADGE_NAME),
        _badge_escape(status_text),
        status_color)


def error_badge():
    """

    :return: A badge denoting that the validation encountered an error
    """
    status_text = 'error'
    status_color = 'red'
    return BADGE_URL.format(
        _badge_escape(BADGE_NAME),
        _badge_escape(status_text),
        status_color)
