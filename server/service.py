from model.running_model import RunningModel
from server.dto.runnning_dto import RunningDto


class RunningService:

    def __init__(self):
        self.running_model = RunningModel()
        self.running_data = self.running_model.create_model()

    def preprocess_data(self):
        response_data = []
        for i in self.running_data:
            running = RunningDto(i[0], i[1], i[2], i[3])
            response_data.append(running)

        return response_data
