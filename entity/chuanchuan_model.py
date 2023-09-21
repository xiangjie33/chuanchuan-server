class PredictorModel:
    def __init__(self, model_path, merge_from_file):
        self._model_path = model_path
        self._merge_from_file = merge_from_file

    def get(self, name, other=None):
        if name == 'model_path':
            return self._model_path
        elif name == 'merge_from_file':
            return self._merge_from_file
        else:
            return None
