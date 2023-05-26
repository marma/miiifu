class HttpException(Exception):
    def __init__(self, message, status_code):
        self.status_code = status_code
        #self.message = message

        super().__init__(self.message)

