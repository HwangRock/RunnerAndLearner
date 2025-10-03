from model.running_repository import RunningRepository
from model.ex_running_repository import ExRunningModel
from server.dto.runnning_dto import RunningDto
from server.dto.ex_running_dto import ExRunningDto


class RunningService:

    def __init__(self):
        self.running_model = RunningRepository()
        self.ex_running_model = ExRunningModel()
        self.running_data = self.running_model.create_model()
        self.ex_running_data = self.ex_running_model.create_model()

    def preprocess_running_data(self):
        response_data = []
        for i in self.running_data:
            running = RunningDto(i.date, i.time, i.distance, i.kcal)
            response_data.append(running)

        return response_data

    def preprocess_ex_running_data(self):
        response_data = []
        for i in self.ex_running_data:
            ex_running = ExRunningDto(i.date, i.name, i.time, i.kcal)
            response_data.append(ex_running)

        return response_data
