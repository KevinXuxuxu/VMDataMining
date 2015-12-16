# -*- coding: utf-8 -*-

__author__ = "Fangzhou Xu"
__email__ = "kevin.xu.fangzhou@gmail.com"

import requests
import json
import re
import web
import numpy
import matplotlib.pyplot as plt

def histogram(d, bins):
    if type(d) == dict:
        d = d.values()
    plt.hist(d, bins=bins)
    plt.show()

def parse(s):
    try:
        return json.loads(s)
    except Exception:
        return s

class GraderJobs:
    """
        Data came from /grader_jobs url
    """

    def __init__(self, url="http://218.247.230.201:8080"):
        self.r = requests.get(url+"/grader_jobs.json")
        self.data = self.r.json()

    def get_correct_rate(self, exp_id=0):
        if exp_id == 0:
            grade = [r['grade'] for r in self.data]
        else:
            grade = [r['grade'] for r in filter(lambda x: parse(x['grader_payload'])['exp_id'] == exp_id, self.data)]
            if len(grade) == 0:
                raise Exception("exp id not found.")

        mark = [(1 if p > 0 else 0) for p in grade]
        return sum(mark) / float(len(mark))

    def get_time_distr(self, exp_id=0):
        if exp_id == 0:
            time = [r['created_at'] for r in self.data]
        else:
            time = [r['created_at'] for r in filter(lambda x: parse(x['grader_payload'])['exp_id'] == exp_id, self.data)]
            if len(time) == 0:
                raise Exception("exp id not found.")

        time = sorted(time)
        parsed_time = map(lambda x:re.split('[A-Z\.\:\-]',x), time)
        res = []
        current_day = ""
        current_count = 0
        for t in parsed_time:
            if t[1:3] != current_day:
                if current_day != "":
                    res += [("%s-%s" %(current_day[0],current_day[1]), current_count)]
                current_day = t[1:3]
                current_count = 1
            else:
                current_count += 1
        res += [("%s-%s" %(current_day[0],current_day[1]), current_count)]
        return res

    def get_code_files(self, exp_id=0, filter_user=True):
        if exp_id == 0:
            filtered_data = self.data
        else:
            filtered_data = [r for r in filter(lambda x: parse(x['grader_payload'])['exp_id'] == exp_id, self.data)]
            if len(filtered_data) == 0:
                raise Exception("exp id not found.")

        if filter_user:
            d = {}
            for sub in filtered_data:
                if sub['grade'] > 0:
                    d[sub['anonym_id']] = sub['code_file']
        else:
            d = {}
            i = 0;
            for sub in filtered_data:
                if sub['grade'] > 0:
                    d[i] = sub['code_file']
                i += 1
        return d

    def code_file_len(self, exp_id=0, filter_user=True):
        d = self.get_code_files(exp_id=exp_id, filter_user=filter_user)
        for k in d.keys():
            d[k] = len(d[k])
        return d

    def code_file_lines(self, exp_id=0, filter_user=True):
        d = self.get_code_files(exp_id=exp_id, filter_user=filter_user)
        for k in d.keys():
            d[k] = len(d[k].split('\n'))
        return d



urls = (
    '/', 'index',
    '/correct_rate(.*)', 'correct_rate',
    '/submit_distribution(.*)', 'submit_distribution'
    '/coding_style(.*)', 'coding_style'
)

class index:
    def GET(self):
        return """
        routes:
            /correct_rate
            /correct_rate/exp_id
            /submit_distribution
            /submit_distribution/exp_id
            /coding_style
            /coding_style/exp_id
            """
class correct_rate:
    def GET(self, name):
        name = name[1:]
        try:
            gd = GraderJobs()
            if name == "":
                return gd.get_correct_rate()
            else:
                try:
                    exp_id = int(name)
                except Exception:
                    raise Exception("Please enter experiment id.")
                return gd.get_correct_rate(exp_id=exp_id)
        except Exception as e:
            return e.message

class submit_distribution:
    def GET(self, name):
        name = name[1:]
        try:
            gd = GraderJobs()
            if name == "":
                return gd.get_time_distr()
            else:
                try:
                    exp_id = int(name)
                except Exception:
                    raise Exception("Please enter experiment id.")
                return gd.get_time_distr(exp_id=exp_id)
        except Exception as e:
            return e.message

class coding_style:
    def GET(self, name):
        name = name[1:]
        try:
            gd = GraderJobs()
            if name == "":
                return gd.coding_style()
            else:
                try:
                    exp_id = int(name)
                except Exception:
                    raise Exception("Please enter experiment id.")
                return gd.coding_style(exp_id=exp_id)
        except Exception as e:
            return e.message

def main():
    app = web.application(urls, globals())
    app.run()

if __name__ == "__main__":
    main()
