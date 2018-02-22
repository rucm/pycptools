import requests
from lxml import html

import re
import json
import codecs


class ProblemList(object):
    base_url = ''
    contest_id = ''
    problems = {}

    def __init__(self, contest_id=None):
        if contest_id is not None:
            self.set_contest_id(contest_id)

    def set_contest_id(self, contest_id):
        self.contest_id = contest_id
        self.base_url = 'https://{}.contest.atcoder.jp'.format(self.contest_id)

    def request(self, url):
        try:
            res = requests.get(url, timeout=30)
        except Exception as e:
            print(e.message)
        else:
            res.raise_for_status()
            return html.fromstring(res.text)

    def get_samples(self, url):
        root = self.request(url)
        elements = root.cssselect('span.lang-ja div.part pre')
        if len(elements) == 0:
            elements = root.cssselect('div#task-statement div.part pre')
        input_format = elements[0].text_content()

        samples = []
        it = iter(elements[1:])
        for _in, _out in zip(it, it):
            samples.append({
                'input': _in.text_content(),
                'output': _out.text_content()
            })

        return input_format, samples

    def add_problem(self, ele):
        tds = ele.cssselect('td')
        url = self.base_url + tds[0].cssselect('a')[0].get('href')
        input_format, samples = self.get_samples(url)

        self.problems[tds[0].text_content()] = {
            'title': tds[1].text_content(),
            'url': url,
            'format': input_format,
            'samples': samples
        }

    def fetch(self):
        root = self.request(self.base_url + '/assignments')
        elements = root.cssselect('tbody tr')
        self.problems = {}

        for ele in elements:
            self.add_problem(ele)

    def save(self, path=''):
        filename = '{}.json'.format(self.contest_id)
        obj = {
            'base_url': self.base_url,
            'problems': self.problems
        }

        with codecs.open(path + filename, 'w', 'utf-8') as file:
            json.dump(obj=obj, fp=file, ensure_ascii=False, indent=4)

    def load(self, filename):
        with codecs.open(filename, 'r', 'utf-8') as file:
            obj = json.load(file)

            url_host = obj['base_url'].split('https://')[1]
            self.contest_id = url_host.split('.')[0]
            self.base_url = obj['base_url']
            self.problems = obj['problems']
