from collections import defaultdict


class Skill:
    def __init__(self, name, level):
        self.name = name
        self.level = level

    def __eq__(self, other_skill):
        return self.name == other_skill.name and self.level == other_skill.level

    def __lt__(self, other_skill):
        return (self.name, self.level) < (other_skill.name, other_skill.level)

    def __repr__(self):
        return f"{self.name} {self.level}"

    def __hash__(self):
        return hash((self.name, self.level))


class Customer:
    def __init__(self, name):
        self.name = name
        self.skills = set()
        self.skills_by_name = {}

    def add_skill(self, skill):
        if skill.name in self.skills:
            print('WARNING! Skill already exists')

        self.skills.add(skill)
        self.skills_by_name[skill.name] = skill

    def upgrade_skill(self, skill):
        self.skills.remove(skill)
        skill.level += 1
        self.skills.add(skill)

    def have_skill(self, skill):
        if skill in self.skills:
            return True

        if skill.name in self.skills_by_name:
            return self.skills_by_name[skill.name].level >= skill.name

        return False

    def __repr__(self):
        return f"{self.name} {self.level}"


class Project:
    def __init__(self, name, points, duration, deadline):
        self.name = name
        self.points = points
        self.start_date = duration
        self.deadline = deadline
        self.requirements = list()

    def add_requirement(self, skill):
        self.requirements.append(skill)

    def __repr__(self):
        return f"{self.name} {self.points}"


def read_file(filepath):
    customers = []
    projects = []

    with open(filepath, 'r') as f:
        customer_count, project_count = list(map(int, f.readline().split()))

        for _ in range(int(customer_count)):
            customer_name, skill_count = f.readline().split()

            customer = Customer(customer_name)

            for _ in range(int(skill_count)):
                skill_name, skill_level = f.readline().split()

                skill = Skill(skill_name, int(skill_level))
                customer.add_skill(skill)

            customers.append(customer)


        for _ in range(project_count):
            project_name, duration, scores, deadline, req_count = f.readline().split()

            project = Project(project_name, int(scores), int(duration), int(deadline))

            for _ in range(int(req_count)):
                skill_name, skill_level = f.readline().split()

                req = Skill(skill_name, int(skill_level))
                project.add_requirement(req)

            projects.append(project)

    return customers, projects


def suitable_requirements(project, customer):
    requirements = list()

    for req in project.requirements:
        if customer.have_skill(req):
            requirements.append(req)

    return requirements


def find_people_for_project(project: Project, customers):
    req_counts = defaultdict(int)

    for customer in customers:
        requirements = suitable_requirements(project, customer)

        for req in requirements:
            req_counts[req] += 1

