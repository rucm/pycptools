import os
import re
import json
import codecs
import shutil
from lxml import html
import cssselect

from .service import Service


CONFIRM_MESSAGE = 'It already exists. Do you want to overwrite? [y/n]\n'
TEMPLATE_SOURCE = '''#include <bits/stdc++.h>
using namespace std;

int main(void) {

    return 0;
}
'''


class Project:

    def __init__(self, service=Service()):
        self.service = service
        self.problems = {}
        self.contest_id = ''

    def download(self, contest_id):
        self.contest_id = contest_id
        url = 'https://{}.contest.atcoder.jp'.format(contest_id)
        res = self.service.request('GET', url + '/assignments')
        root = html.fromstring(res.text)
        self._set_problems(url, root.cssselect('tbody tr'))

    def create(self):
        assert len(self.problems) > 0, 'Can\'t create project.'
        self._make_dir(self.contest_id)
        self._write_properties(self.contest_id)
        self._export_template(self.contest_id)

    def _set_problems(self, url, elements):
        self.problems = {}
        for ele in elements:
            tds = ele.cssselect('td')
            self.problems[tds[0].text_content()] = {
                'title': tds[1].text_content(),
                'url': url + tds[0].cssselect('a')[0].get('href'),
                'task-id': self._parse_to_task_id(tds[4])
            }
            self._set_samples(tds[0].text_content())

    def _parse_to_task_id(self, td):
        reg = re.compile(r'\/submit\?task_id=([0-9]+)')
        href = td.cssselect('a')[0].get('href')
        m = reg.match(href)
        return m.group(1)

    def _set_samples(self, problem_id):
        assert problem_id in self.problems, 'This problem_id does not exists.'
        res = self.service.request('GET', self.problems[problem_id]['url'])
        root = html.fromstring(res.text)
        elements = root.cssselect('span.lang-ja div.part')
        if len(elements) == 0:
            elements = root.cssselect('div#task-statement div.part')
        _in, _out = [], []
        _format = ''
        for ele in elements:
            h3 = ele.cssselect('h3')
            if len(h3) == 0:
                continue
            if h3[0].text_content().startswith('入力例'):
                _in.append(ele.cssselect('pre')[0].text_content())
            elif h3[0].text_content().startswith('出力例'):
                _out.append(ele.cssselect('pre')[0].text_content())
            elif h3[0].text_content().startswith('入力'):
                _format = ele.cssselect('pre')[0].text_content()
        _samples = [{'in': i, 'out': o} for i, o in zip(_in, _out)]
        self.problems[problem_id]['format'] = _format
        self.problems[problem_id]['samples'] = _samples

    def _make_dir(self, path):
        if os.path.exists(path):
            if self._confirm():
                self._remove_dirs(path)
            else:
                return
        os.mkdir(path)
        os.mkdir(os.path.join(path, 'src'))

    def _confirm(self):
        while True:
            choise = input(CONFIRM_MESSAGE).lower()
            if choise in ['y', 'ye', 'yes']:
                return True
            elif choise in ['n', 'no']:
                return False

    def _remove_dirs(self, path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(path)

    def _write_properties(self, path):
        properties_file = os.path.join(path, 'properties.json')
        obj = {'contest-id': self.contest_id, 'problems': self.problems}
        with codecs.open(properties_file, 'w', 'utf-8') as f:
            json.dump(obj=obj, fp=f, ensure_ascii=False, indent=4)

    def _export_template(self, dir_path):
        for problem_id in self.problems.keys():
            path = os.path.join(dir_path, 'src', '{}.cpp'.format(problem_id))
            with open(path, 'w') as f:
                f.write(TEMPLATE_SOURCE)
