#!/usr/bin/python

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
        testmessage = "commit 3942e0aaf204569b8c123c4864ff1f630de70969\nAuthor: Alfonso Roman <aroman@oid.ucla.edu>\nDate:   Tue Jul 30 14:45:13 2013 -0700\n\nfirst commit\n\nphpunit: @javascript @what @test2\n\nA     dispatcher.py\nA     course/test/dummy_test.php\nM     course/test/dummy2_test.php"
        for f in glob.glob("./parsers/parser_*.py"):
            
            # module = re.search(r'_.*\.py', f).group(0)

            parser = imp.load_source('Parser', f)
            p = parser.Parser(testmessage)
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

