class FakeLCMAPHTTP(object):

    def __init__(self, fake_response):
        self.fake_response = fake_response

    def get(self, *args, **kwargs):
        return self.fake_response


class FakeLCMAPRESTResponse(object):

    def __init__(self, data):
        self.data = data
        self.result = data["result"]

