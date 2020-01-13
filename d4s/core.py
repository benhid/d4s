from d4s.context import context


class Data4Science:

    def __init__(self, options: dict = None):
        # update context with options
        context.update(**options)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __repr__(self) -> str:
        template = '<{cls}: name="{self.name}">'
        return template.format(cls=type(self).__name__, self=self)
