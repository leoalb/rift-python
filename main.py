import argparse
import logging

import config
import rift

def log_level(string):
    string = string.lower()
    if string == 'critical':
        return logging.CRITICAL
    elif string == 'error':
        return logging.ERROR
    elif string == 'warning':
        return logging.WARNING
    elif string == 'info':
        return logging.INFO
    elif string == 'debug':
        return logging.DEBUG
    else:
        msg = "{} is not a valid log level".format(string)
        raise argparse.ArgumentTypeError(msg)

def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='Routing In Fat Trees (RIFT) protocol engine')
    parser.add_argument('configfile', nargs='?', default='', help='Configuration filename')
    passive_group = parser.add_mutually_exclusive_group()
    passive_group.add_argument('-p', '--passive', action="store_true", help='Run only the nodes marked as passive')
    passive_group.add_argument('-n', '--non-passive', action="store_true", 
        help='Run all nodes except those marked as passive')
    parser.add_argument('-l', '--log-level', type=log_level, default='info',
        help='Log level (debug, info, warning, error, critical)')
    args = parser.parse_args()
    return args

def active_nodes(args):
    if args.passive:
        return rift.Rift.ActiveNodes.ONLY_PASSIVE_NODES
    elif args.non_passive:
        return rift.Rift.ActiveNodes.ALL_NODES_EXCEPT_PASSIVE_NODES
    else:
        return rift.Rift.ActiveNodes.ALL_NODES

if __name__ == "__main__":
    args = parse_command_line_arguments()
    config = config.parse_configuration(args.configfile)
    rift_object = rift.Rift(active_nodes(args), args.log_level, config)
    rift_object.run()