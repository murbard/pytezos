class FeesProvider:

    def get_fees(self, kind):
        raise NotImplementedError


class Athens004FeesProvider(FeesProvider):

    def get_fees(self, kind):
        pass
