#!/bin/python

from parsers import parser

#
# PHPUnit parser
#
import re
import StringIO
from pprint import pprint

class Parser(parser.ParserBase):

    def __init__(self, msg):
        parser.ParserBase.__init__(self, msg)
        self.fields = {}
        self.command = 'vendor/bin/phpunit'
        self.params = [
            "--log-junit '/coverage/unitreport.xml'",
            "--coverage-html '/coverage'",
            "--coverage-clover '/coverage/coverage.xml'"
        ]

    def parse(self):
        commitmsg = StringIO.StringIO(self.msg)       
        ret = False
        # Get SHA
        commitline = commitmsg.readline()
        match = re.match(r"commit (\w+)", commitline)
        if match:
            self.fields['sha'] = match.group(1)

        # Get commit author
        authorline = commitmsg.readline()
        match = re.match(r"Author: (?P<firstname>\w+) (?P<lastname>\w+) <(?P<email>.+@[\w+\.]+\w+)>", authorline)
        if match:    
            author = match.groupdict()
            self.fields = dict(self.fields.items() + author.items())

        # Get date
        dateline = commitmsg.readline()
        match = re.match(r"Date:\s*(.*)", dateline)
        if match:
            self.fields['date'] = match.group(1)

        # Get commit message body, PHPUnit hooks, and _test.php files altered
        body = ""
        test_files = []
        for line in commitmsg.readlines():
            
            # Try to match phpunit tags
            match = re.match(r"phpunit:\s*@(\S+)+", line)
            if match:
                tags = re.findall(r"(@\S+)", line)
                self.fields['phpunit'] = tags
                
                # Add a --group param
                groupopt = "--group " + ','.join(tags) 
                self.params.append(groupopt)
                ret = True
                
            # Try to match altered files ending in _test.php
            match = re.match(r"[AM]\s*(\S+_test.php)", line)
            if match:
                test_files.append(match.group(1))
            body += line
        
        if body:
            self.fields['body'] = body
            
        if test_files:
            self.fields['test_files'] = test_files
            # Add files as command params if tags weren't given
            if not ret:
                groupopt = ' '.join(test_files) 
                self.params.append(groupopt)
                ret = True
    
        return ret
