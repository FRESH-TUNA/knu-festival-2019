class PostsCommentsDeactiveService:
    def __init__(self, *args, **kwargs):
        self.instance = None

        for key, value in kwargs.items():
            setattr(self, key, value)

    def call(self):
        instance = self.instance
        instance.content = ""
        instance.password = ""
        instance.active = False
        instance.save()
