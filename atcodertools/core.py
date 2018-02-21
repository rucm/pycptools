import fire

from .problem_list import ProblemList


class Commands(object):

    def fetch(self, contest_id):
        problem_list = ProblemList(contest_id)
        problem_list.fetch()
        problem_list.save()

    def create(self, contest_id=None, filename=None):
        if contest_id is not None:
            problem_list = ProblemList(contest_id)
            problem_list.fetch()
            print('problem fetch success')
        elif filename is not None:
            problem_list = ProblemList()
            problem_list.load(filename)
            print('problem load success')


def main():
    fire.Fire(Commands)

if __name__ == '__main__':
    main()
