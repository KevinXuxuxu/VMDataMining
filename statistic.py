# -*- coding: utf-8 -*-

__author__ = "Fangzhou Xu"
__email__ = "kevin.xu.fangzhou@gmail.com"

import requests
import json
import re

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

def main():
    gd = GraderJobs()
    print gd.get_time_distr(exp_id=2)

if __name__ == "__main__":
    main()
