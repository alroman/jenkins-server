#!/bin/python

from parsers import parser

#
# PHPUnit parser
#

import re

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
        ret = False
        
        # Get commit message body, PHPUnit hooks, and _test.php files altered
        body = ""
        test_files = []
        tags = []
        for line in self.msgIO.readlines():
            
            # Try to match phpunit tags
            match = re.match(r"phpunit:\s*@(\S+)+", line)
            if match:
                tags = tags + re.findall(r"@(\S+)", line)
                
            # Try to match altered files ending in _test.php
            else:
                match = re.match(r"[AM]\s*(\S+_test.php)", line)
                if match:
                    test_files.append(match.group(1))
            # Build message body
            body += line
        
        # Add fields to dictionary and build command params
        if body:
            self.fields['body'] = body
            
        if tags:
            self.fields['phpunit'] = tags
            # Add tags as a --group command param
            groupopt = "--group " + ','.join(tags) 
            self.params.append(groupopt)
            ret = True
            
        if test_files:
            self.fields['test_files'] = test_files
            # Add files as command params if tags weren't given
            if not tags:
                groupopt = ' '.join(test_files) 
                self.params.append(groupopt)
                ret = True
    
        return ret
