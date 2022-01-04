from .examples import PopulateExamples


class PopulateDB:
    def __init__(self):
        self.run()

    def run(self):
        PopulateExamples().run()
