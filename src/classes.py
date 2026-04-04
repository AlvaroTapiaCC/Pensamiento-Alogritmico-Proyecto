class Task:
    def __init__(self, id, duration, category):
        self.id = id
        self.duration = int(duration)
        self.category = category

    def get_category(self):
        return self.category
    
    def get_duration(self):
        return self.duration


class Resource():
    def __init__(self, id, categories: list):
        self.id = id
        self.categories = categories
        self.total_duration = 0
        self.assigned_tasks = []

    def get_categories(self):
        return self.categories
    
    def add_duration(self, duration):
        self.total_duration += duration

    def add_task(self, task: Task):
        self.assigned_tasks.append(task)
        self.add_duration(task.duration)




class Planner():
    def __init__(self, resources: list[Resource], tasks: list[Task]):
        self.resources = resources
        self.tasks = tasks
        self.schedule = []


    def find_available_resource(self, category):
        chosen = None
        for resource in self.resources:
            if category in resource.categories:
                if chosen is None or resource.total_duration < chosen.total_duration:
                    chosen = resource
        return chosen

    def assign_task(self, task: Task):
        resource = self.find_available_resource(task.category)
        start_time = resource.total_duration
        end_time = resource.total_duration + task.duration
        resource.add_task(task)
        self.schedule.append((task.id, resource.id, start_time, end_time))

    def write_schedule(self):
        with open("data/output.txt", "w") as o_file:
            for s in self.schedule:
                o_file.write(f"{s[0]},{s[1]},{s[2]},{s[3]}\n")


    def solve(self):
        for task in self.tasks:
            self.assign_task(task)
        self.write_schedule()
