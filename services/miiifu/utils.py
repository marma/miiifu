from werkzeug.routing import BaseConverter

class HttpException(Exception):
    def __init__(self, message, status_code):
        self.status_code = status_code
        #self.message = message

        super().__init__(message)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


