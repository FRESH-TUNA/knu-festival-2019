class PasswordValidationService:
    def __init__(self, *args, **kwargs):
        self.instance_password = None
        self.request_password = None

        for key, value in kwargs.items():
            setattr(self, key, value)

    def call(self):
        return self.instance_password == self.request_password
