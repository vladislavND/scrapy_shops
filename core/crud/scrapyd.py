import os
import logging

import requests

from datetime import datetime


logger = logging.getLogger('cms')

HOST = os.getenv('SCRAPYD_HOST')
PORT = os.getenv('SCRAPYD_PORT')
NAME_PROJECT = os.getenv('SCRAPYD_PROJECT_NAME')


class ScraydAPI:
    def __init__(self, host='127.0.0.1', port='6800', project=NAME_PROJECT):
        self.base_url = "http://{}:{}".format(host, port)
        self.project = project

    def daemonstatus(self):
        response = requests.get("{}/daemonstatus.json".format(self.base_url))
        return response.json()

    def schedule(self, project: str, spider: str = None):
        data = {
            "project": project,
            "spider": spider,
            "jobid": datetime.utcnow().strftime('%d-%m-%Y:%H:%M:%S')
        }

        logger.info(data)

        response = requests.post("{}/schedule.json".format(self.base_url), data=data)
        return response.json()

    def listjobs(self, project: str):
        params = {
            'project': project
        }
        response = requests.get("{}/listjobs.json".format(self.base_url), params=params)
        return response.json()

    def listspiders(self, project: str):
        params = {
            'project': project
        }
        response = requests.get("{}/listspiders.json".format(self.base_url), params=params)
        return response.json()

    def cancel(self,  project: str, job: str):
        params = {
            'project': project,
            'job': job
        }
        response = requests.post("{}/cancel.json".format(self.base_url), params=params)
        return response.json()


crud_scrapyd = ScraydAPI()