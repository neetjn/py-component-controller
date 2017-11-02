class Resource(object):

    def __init__(self, **kwargs):
        """
        :Description: Base object for shenanigans.
        """

        required_fields = self.meta.get('required_fields', None)
        if required_fields and not any(field not in fields for field in check.iterkeys()):
            raise AttributeError('Required fields "{}" were not available'.format(required_fields))
 
        for prop, val in kwargs.iteritems():
            setattr(self, prop, val)
