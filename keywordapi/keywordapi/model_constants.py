

class KeywordConstants:
    # TYPE contains the choices available for a keyword type
    TYPES = (
            ('A', 'Must contain'),
            ('O', 'May contain'),
            ('N', 'Must not contain'),
        )

    @classmethod
    def list_comprehension(cls):
        type_choices = [i[0] for i in cls.TYPES]
        return type_choices
