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
        self.time_needed = 0
        self.assigned_tasks = []

    def get_categories(self):
        return self.categories
    
    def add_duration(self, duration):
        self.time_needed += duration

    def add_task(self, task: Task):
        self.assigned_tasks.append(task)




class Planner():
    def __init__(self, resources: list[Resource], tasks: list[Task]):
        self.resources = resources
        self.tasks = tasks
        self.schedule = []


    def find_available_resource(self, category):
        chosen = None
        for resource in self.resources:
            if category in resource.categories:
                if chosen is None or resource.time_needed < chosen.time_needed:
                    chosen = resource
        return chosen

    def assign_task(self, task: Task):
        resource = self.find_available_resource(task.category)
        resource.add_task(task)

    def solve(self):
        for task in self.tasks:
            self.assign_task(task)
