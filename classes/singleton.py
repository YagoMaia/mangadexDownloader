class Singleton:
    """
    Classe responsável por deixar apenas uma isntância existênte, não irá criar outra conexão com banco
    """

    def __init__(self, klass):
        self.klass = klass
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.klass(*args, **kwargs)
        return self.instance
