class Resource(object):

    def __init__(self, **kwargs):
        """
        :Description: Base object for shenanigans.
        """
        for prop, val in kwargs.iteritems():
            setattr(self, prop, val)
