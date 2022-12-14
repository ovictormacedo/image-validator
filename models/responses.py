class CrawlerResponse():
    def __init__(self, status, object):
        self.status = status
        self.object = object

class ValidationResponse():
    def __init__(self, is_valid, object):
        self.is_valid = is_valid
        self.object = object