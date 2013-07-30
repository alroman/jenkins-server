#!/bin/python

from parsers import parser

#
# PHPUnit parser
#

class Parser(parser.ParserBase):

    def __init__(self, msg):
        parser.ParserBase.__init__(self, msg)
        
        self.command = 'vendor/bin/phpunit'
        self.params = [
            "--log-junit '/coverage/unitreport.xml'",
            "--coverage-html '/coverage'",
            "--coverage-clover '/coverage/coverage.xml'"
        ]

    def parse(self):
        # @todo: implement
        pass

