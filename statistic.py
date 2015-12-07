# -*- coding: utf-8 -*-

__author__ = "Fangzhou Xu"
__email__ = "kevin.xu.fangzhou@gmail.com"

import requests
import json

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
            self.grade = [r['grade'] for r in self.data]
        else:
            self.grade = [r['grade'] for r in filter(lambda x: parse(x['grader_payload'])['exp_id'] == exp_id, self.data)]

        mark = [(1 if p > 0 else 0) for p in self.grade]
        try:
            return sum(mark) / float(len(mark))
        except ZeroDivisionError:
            raise Exception("exp id not found")
