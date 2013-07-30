#!/bin/python

import glob
import re
import sys
import getopt
import imp

class Environment:
    def set(self, attr, val):
        attr = attr.lstrip('-')
        self.__dict__[attr] = val

class JobRunner:

    def __init__(self, msg):
        self.msg = msg
        
    def run(self):
        self.runParsers()

    def runParsers(self):
        for f in glob.glob("./parsers/parser_*.py"):
            
            # module = re.search(r'_.*\.py', f).group(0)

            parser = imp.load_source('Parser', f)
            p = parser.Parser('test')
            p.dispatch()
            

def main(argv):

    env = Environment()
    msg = 'foobar'

    try:
        opts, args = getopt.getopt(argv, "h", ['help', 'workspace='])
    except getopt.GetoptError:
        print "jobrunner.py --workspace=$WORKSPACE --op=$OP"
        sys.exit(2)

    # Store environment vars
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print "help!"
        else:
            env.set(opt, arg)

    jobs = JobRunner(msg)
    jobs.run()

if __name__ == "__main__":
    main(sys.argv[1:])

