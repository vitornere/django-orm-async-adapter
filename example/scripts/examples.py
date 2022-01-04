from example.models import Example


class PopulateExamples:
    # Create 50 fake examples
    def run(self):
        for i in range(50):
            Example.objects.create(
                name=f'Example {i}',
                description=f'Description of Example {i}'
            )
