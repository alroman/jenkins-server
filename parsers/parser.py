#!/bin/python

#
# Parser abstract class
#

class ParserBase:

    def __init__(self, msg):
        self.msg = msg
        self.command = ''
        self.params = []

    def parse(self):
        raise NotImplementedError()

    def dispatch(self):

        if self.parse():

            cmd = self.command

            # Create command with params
            for p in self.params:
                cmd += " " + p

            print cmd
