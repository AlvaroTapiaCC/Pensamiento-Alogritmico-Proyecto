from src.classes import Task, Resource, Planner
from src.utils import *
import sys


class Data:
    def __init__(self):
        self.resources = []
        self.tasks = []

    def read_data(self):
        with open("data/recursos.txt", "r") as r_file:
            for line in r_file:
                r = line.strip().split(",")
                resource = Resource(r[0], r[1:])
                self.resources.append(resource)
        with open("data/tareas.txt", "r") as t_file:
            for line in t_file:
                t = line.strip().split(",")
                task = Task(t[0], t[1], t[2])
                self.tasks.append(task)    




def main():
    data = Data()
    data.read_data()
    data.tasks = merge_sort(data.tasks)

    task_manager = Planner(data.resources, data.tasks)
    task_manager.solve()
    mi_makespan = max(r.total_duration for r in task_manager.resources)
    if len(sys.argv) > 1:
        makespan_obj = int(sys.argv[1])
        if mi_makespan <= makespan_obj:
            print(f"Good makespan: {mi_makespan}")
        else:
            print(f"Bad makespan: {mi_makespan}")
    print("Done")


if __name__ == "__main__":
    main()
