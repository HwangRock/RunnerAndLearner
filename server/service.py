from model.running_model import Model
from dto.runnning_dto import RunningDto
import json


class RunningService:

    def __init__(self):
        self.model = Model()
        self.running_data = self.model.create_model()

    def preprocess_data(self):
        response_data = []
        for i in self.running_data:
            running = RunningDto(i[0], i[1], i[2], i[3])
            data = json.dumps(running.__dict__)
            response_data.append(data)

        return response_data
