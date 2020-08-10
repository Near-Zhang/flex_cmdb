from abc import ABC, abstractclassmethod
from event.job import BaseJob


class AbstractTask(BaseJob):

    def name(self):
        pass


    def _run(self):
        pass