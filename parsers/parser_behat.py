#!/bin/python

from parsers import parser

#
# Behat parser
#

import re

class Parser(parser.ParserBase):

    def __init__(self, msg):
        parser.ParserBase.__init__(self, msg)
        self.fields = {}
        self.command = 'vendor/bin/behat'
        self.params = [
            "--config /path/to/your/CFG_behat_dataroot/behat/behat.yml",
            "--format=pretty"
        ]

    def parse(self):
        ret = False
        
        # Get commit message body, PHPUnit hooks, and _test.php files altered
        body = ""
        test_files = []
        tags = []
        for line in self.msgIO.readlines():
            
            # Try to match phpunit tags
            match = re.match(r"behat:\s*(@\S+)+", line)
            if match:
                tags = tags + re.findall(r"(@\S+)", line)
                
            # Build message body
            body += line
        
        # Add fields to dictionary and build command params
        if body:
            self.fields['body'] = body
            
        if tags:
            self.fields['behat'] = tags
            # Add tags as a --group command param
            tagstr = ','.join(tags)
            tagsopt = "--tags '" + tagstr + "'"
            self.params.append(tagsopt)
            ret = True
    
        return ret

