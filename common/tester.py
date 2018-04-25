import os
import json
import codecs
import subprocess
import click
from .service import Service


class Tester:

    def __init__(self, service=Service()):
        self.service = service
        self.properties = {}

        with codecs.open('properties.json', 'r', 'utf-8') as f:
            self.properties = json.load(f)

    def test(self, problem_id, command='./a.exe'):
        samples = self.properties['problems'][problem_id.upper()]['samples']
        click.echo('test cases : {}'.format(len(samples)))

        source_file = os.path.join('src', '{}.cpp'.format(problem_id.upper()))

        returncode, _ = self._compile(source_file)
        click.echo('compile : {}'.format('OK' if returncode == 0 else 'CE'))
        if returncode == 1:
            return

        for i, sample in enumerate(samples):
            click.echo('case {}:'.format(i + 1))
            r, o = self._compare(command, sample['in'], sample['out'])
            click.echo('{}'.format('AC' if r else 'WA'))
            if not r:
                click.echo('output:')
                click.echo('{}'.format(o))

    def _compare(self, command, in_data='', out_data=''):
        p = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            encoding='utf-8'
        )
        out = p.communicate(in_data)[0]

        _out = ' '.join(out.splitlines())
        _out_data = ' '.join(out_data.splitlines())
        return _out == _out_data, out

    def _compile(self, filename):
        p = subprocess.run(
            ('g++', filename, '-std=c++14'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return p.returncode, p.stderr
