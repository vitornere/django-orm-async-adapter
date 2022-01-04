from example.models import Example


class CleanDB:
    def __init__(self):
        self.run()

    # Delete all examples
    def run(self):
        Example.objects.all().delete()
