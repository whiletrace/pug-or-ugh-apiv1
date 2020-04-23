class StatusConverter:
    """ class encapsulates logic for custom URL converter

        attributes:
            regex
                regex pattern that wil be matched in the URL
        methods:
            to_python, to_url

    See `django custom path converters
    <https://docs.djangoproject.com/en/3.0/topics/http
    /urls/#registering-custom-path-converters>`_ for info
    """
    regex = 'liked|disliked|undecided'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return '%s' % value
