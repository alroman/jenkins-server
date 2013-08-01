#!/bin/python

#
# Parser abstract class
#
import re
import StringIO
from pprint import pprint 

class ParserBase:

    def __init__(self, msg):
        self.msg = msg
        self.msgIO = StringIO.StringIO(msg)
        self.fields = {}
        self.command = ''
        self.params = []

    def parse(self):
        raise NotImplementedError()
    
    def parseHeader(self):
        # Get SHA
        commitline = self.msgIO.readline()
        match = re.match(r"commit (\w+)", commitline)
        if match:
            self.fields['sha'] = match.group(1)

        # Get commit author and email
        authorline = self.msgIO.readline()
        match = re.match(r"Author: (?P<firstname>\w+) (?P<lastname>\w+) <(?P<email>.+@[\w+\.]+\w+)>", authorline)
        if match:    
            author = match.groupdict()
            self.fields = dict(self.fields.items() + author.items())

        # Get date
        dateline = self.msgIO.readline()
        match = re.match(r"Date:\s*(.*)", dateline)
        if match:
            self.fields['date'] = match.group(1)

    def dispatch(self):
        
        self.parseHeader()
        
        if self.parse():
            pprint(self.fields)
            cmd = self.command

            # Create command with params
            for p in self.params:
                cmd += " " + p

            print cmd
