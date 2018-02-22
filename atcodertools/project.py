import os

from .problem_list import ProblemList


class Project(object):
    project_path = ''

    def create(self, problem_list: ProblemList):
        self.project_path = problem_list.contest_id

        os.mkdir(self.project_path)
        problem_list.save(self.project_path + '/')
        for tag, problem in problem_list.problems.items():
            self.add_problem(tag, problem)

    def create_home_dir(self, path):
        pass

    def add_problem(self, tag, problem):
        os.makedirs('{}/{}'.format(self.project_path, tag))
