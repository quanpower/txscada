#!/usr/bin/env python2
# encoding: utf-8

import sys
import utils
import errors
print utils
import logging
logger = logging.getLogger('')


def runcommand(cmdline, options, command_dict):
    """Split commands in fabric style,
    returns (cmdname, cmdkwargs)"""
    if ':' in cmdline:
        cmdname, args = cmdline.split(':', 1)
    else:
        cmdname, args = cmdline, ''
    #print cmdname, "-", args
    command_name = utils.choose(cmdname, command_dict.keys())

    name = command_name        
    command_func = command_dict[name]
    try:
        kwargs = utils.make_kwargs(command_func, args)
    except ValueError as e:
        raise errors.CommandArgumentError(unicode(e))
    return command_func(options, **kwargs)
    
def setup_logging(options):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%d-%m-%y %H:%M',
                        filename='automata.log',
                        filemode='w')
    if options.verbose:
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)
    
    
    

def main(argv = sys.argv):
    # Aplicación
    
    from commands import COMMANDS
    from options import parser
    
    options = parser.parse_args()
    setup_logging(options)
    try:
        return runcommand(options.command[0], options, command_dict=COMMANDS)
    except errors.NoSuchCommand as e:
        print e
    except errors.CommandArgumentError as e:
        print "Command Argument Error: %s" % e
    return -1
    

if __name__ == "__main__":
    sys.exit(main())