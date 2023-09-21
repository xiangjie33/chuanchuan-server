class PredictorData:
    def __init__(self, thing_classes):
        self._thing_classes = thing_classes

    def get(self, name, other=None):
        if name == 'thing_classes':
            return self._thing_classes
        else:
            return None
