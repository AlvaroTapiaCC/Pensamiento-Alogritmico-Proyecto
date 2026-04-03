from classes import Task, Resource, Planner
from utils import *


class Data:
    def __init__(self):
        self.resources = []
        self.tasks = []

    def read_data(self):
        with open("recursos.txt", "r") as r_file:
            for line in r_file:
                r = line.strip().split(",")
                resource = Resource(r[0], r[1:])
                self.resources.append(resource)
        with open("tareas.txt", "r") as t_file:
            for line in t_file:
                t = line.strip().split(",")
                task = Task(t[0], task[1], task[2])
                self.tasks.append(task)    




def main():
    data = Data()
    data.read_data()
    data.tasks = merge_sort(data.tasks)

    task_planner = Planner(data.resources, data.tasks)
    task_planner.solve()


if __name__ == "__main__":
    main()
