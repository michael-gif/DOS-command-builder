import argparse

from typing import Callable


class DOS_Command:
    def __init__(self, keyword: str):
        self.keyword = keyword
        self.parser = argparse.ArgumentParser()
        self.parser.prog = keyword
        self.syntax = ''
        self.callback = None

    def add_arg_required(self, arg: dict):
        '''
        | Check the format of the argument given, checking the keys and the type of the name.
        | Then add it to the parser.
        :param arg: dict
        :return:
        '''
        if 'name' not in arg:
            raise KeyError("each argument must have a 'name' property")
        if type(arg['name']) != str:
            raise KeyError(f"the 'name' property must be a string")

        if 'type' not in arg:
            raise KeyError(f"arg {arg['name']} must have a 'type' property")

        self.parser.add_argument(arg['name'], type=arg['type'])

    def add_arg_optional(self, arg: dict):
        '''
        | Check the format of the argument given, checking the keys and the type of the name.
        | Then add it to the parser.
        :param arg: dict
        :return:
        '''
        if 'name' not in arg:
            raise KeyError("each argument must have a 'name' property")
        if type(arg['name']) != str:
            raise KeyError(f"the 'name' property must be a string")

        if 'type' not in arg:
            raise KeyError(f"arg {arg['name']} must have a 'type' property")

        self.parser.add_argument('-' + arg['name'], type=arg['type'])

    def generate_syntax(self):
        '''
        | Generates the syntax for a command by extracting it from 'parser.format_usage()'
        | Optional arguments are put first, then required arguments at the end
        :return:
        '''
        self.syntax = self.parser.format_usage()[7:-1]


registered_commands = {}
debug = False


def dos_command(attributes: dict):
    '''
    | Used to decorate functions that will be used as callbacks for commands
    | Creates an instance of DOS_Command, which contains the command keyword, its arguments, and the syntax
    :param attributes:
    :return: Decorator
    '''

    if not attributes:
        raise TypeError("attributes argument cannot be empty")
    if type(attributes) != dict:
        raise TypeError(f"attributes must be a dictionary. instead got {type(attributes)}")

    def wrapper(function):
        '''
        Create an instance of DOS_Command, giving it the function as a callback, and adding all of the specified arguments from the attributes dict
        :param function:
        :return:
        '''

        callback: Callable = function

        # null check the attributes
        if 'keyword' not in attributes:
            attributes['keyword'] = callback.__name__
        if 'args.required' not in attributes:
            raise KeyError("could not find 'args.required' in attributes")
        if 'args.optional' not in attributes:
            raise KeyError("could not find 'args.optional' in attributes")

        # type check 'args.required' and 'args.optional'
        if type(attributes['args.required']) != list:
            raise TypeError(
                f"'args.required' must be a list. instead got {type(attributes['args.required'])}")
        if type(attributes['args.optional']) != list:
            raise TypeError(
                f"'args.optional' must be a list. instead got {type(attributes['args.optional'])}")

        # create the command instance and add it to the register
        new_command = DOS_Command(attributes['keyword'])
        for arg in attributes['args.required']:
            new_command.add_arg_required(arg)
        for arg in attributes['args.optional']:
            new_command.add_arg_optional(arg)
        new_command.generate_syntax()
        if debug:
            print('[INFO] Registered new command: ' + new_command.syntax)

        new_command.callback = callback
        registered_commands[new_command.keyword] = new_command

    return wrapper


def run_command(command: str):
    # separate the command into its keyword and an argument list
    sections = command.split(" ", 1)
    command_keyword = sections[0]
    command_args = sections[1] if len(sections) == 2 else ''
    args_list = command_args.split(' ') if command_args else []

    # find the relevant dos command
    if command_keyword not in registered_commands:
        print(f"'{command_keyword}' is not recognized as a command")
        return
    relevant_dos_command: DOS_Command = registered_commands[command_keyword]

    # parse the args list. then execute the command, giving it the parsed args
    parsed_args = vars(relevant_dos_command.parser.parse_args(args_list))
    if not parsed_args:
        parsed_args = []
    exit_code = relevant_dos_command.callback(parsed_args, len(parsed_args.keys()))
    return exit_code
