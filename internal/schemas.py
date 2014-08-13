__author__ = 'Gareth Coles'


class Type(object):
    def __init__(self, *args):
        self.types = args

    def validate(self, obj):
        for typ in self.types:
            if obj is typ or isinstance(obj, typ):
                return True
        return False


SAMPLE = {
    "version": Type(int),  # For updates
    "base_url": Type(str),  # For relative URL paths and such
    "name": Type(str, None),  # The site's name
    "logo": Type(str),  # URL to the site logo
}

schemas = {
    "sample": SAMPLE,  # Sample schema
}
