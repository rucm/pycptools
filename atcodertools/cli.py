import click
from .tester import Tester
from .project import Project
from .service import Service


@click.group()
def atcodertools():
    pass


@atcodertools.command()
@click.argument('contest-id')
def create(contest_id):
    Project().create(contest_id)


@atcodertools.command()
def login():
    Service().login()


@atcodertools.command()
def logout():
    Service().logout()


@atcodertools.command()
@click.argument('problem-id')
def test(problem_id):
    Tester().test(problem_id)


@atcodertools.command()
@click.argument('problem-id')
def submit(problem_id):
    click.echo('submit')


if __name__ == '__main__':
    atcodertools()
