class DOS_ArgumentParser:
    def parse(self, string_args: str):
        '''
        Parses a string of arguments into a list of dictionaries, each dict being an argument
        :param string_args:
        :return: list
        '''
        parsed_args = []
        args = string_args.split(" ")
        for arg in args:
            parsed_argument = self._parse_single_argument(arg)
            parsed_args.append(parsed_argument)
        return parsed_args

    def _parse_single_argument(self, arg):
        '''
        Parses a single argument into a dictionary. For internal use only.
        :param arg:
        :return: dict
        '''
        parsed_arg = {
            'name': None,
            'value': None
        }
        if '=' in arg:
            pair = arg.split('=', 1)
            parsed_arg['name'] = pair[0]
            parsed_arg['value'] = pair[1]
        else:
            parsed_arg['value'] = arg
        return parsed_arg


class DOS_Command:
    def __init__(self, keyword: str):
        self.keyword = keyword
        self.arguments = []
        self.required_args = []
        self.optional_args = []
        self.syntax = ''
        self.callback = None

    def add_argument(self, arg: dict):
        '''
        Check the format of each argument given, checking the keys and the type of the value
        :param arg: dict
        :return:
        '''
        if 'name' not in arg:
            raise KeyError("each argument must have a 'name' property")
        if type(arg['name']) != str:
            raise KeyError(f"the 'name' property must be a string")

        if 'type' not in arg:
            raise KeyError(f"arg {arg['name']} must have a 'type' property")

        if 'required' not in arg:
            raise KeyError(f"arg {arg['name']} must have a 'required' property")
        if type(arg['required']) != bool:
            raise KeyError(f"the 'required' property must be a boolean")

        if arg['required']:
            self.required_args.append(arg)
        else:
            self.optional_args.append(arg)

        # self.arguments.append(arg)

    def generate_syntax(self):
        '''
        Generates the syntax for a command.
        Optional arguments are put first, then required arguments at the end
        :return:
        '''
        self.syntax = self.keyword
        for arg in self.optional_args:
            self.syntax += f" [{arg['name']}]"
        for arg in self.required_args:
            self.syntax += f" <{arg['name']}>"
        self.syntax = self.syntax.rstrip()

    def check_syntax(self, args: list):
        '''
        Checks the syntax of the given arguments against the required and optional arguments of this command.
        If some of the required arguments are missing, a syntax error is raised.
        If nothing is found wrong with the given arguments, then the detected arguments are returned.

        The arguments will be looped through in reverse order to make it easier to identify the required arguments
        first.
        :param args:
        :return: dict
        '''
        args.reverse()

        # arguments must be exclusively keyword arguments or not keyword arguments
        num_keyword_args, num_optional_args = 0, 0
        for arg in args:
            if arg['name']:
                num_keyword_args += 1
            else:
                num_optional_args += 1
        if num_keyword_args and num_optional_args:
            raise SyntaxError("arguments must be either keyword arguments or value arguments, not both")
        using_keyword_args = True if num_keyword_args else False

        required = {arg['name']: None for arg in self.required_args}
        optional = {arg['name']: None for arg in self.optional_args}
        keys = list(required.keys()) + list(optional.keys())

        # detect the arguments
        if using_keyword_args:
            for arg in args:
                arg_name = arg['name']
                if arg_name in keys:
                    if arg_name in required:
                        required[arg_name] = arg['value']
                    else:
                        optional[arg_name] = arg['value']
                else:
                    raise SyntaxError(f"unknown argument: '{arg_name}'\nsyntax: {self.syntax}")
        else:
            index = 0
            for arg in args:
                current_key = keys[index]
                if current_key in required:
                    required[current_key] = arg['value']
                else:
                    optional[current_key] = arg['value']
                index += 1

        # check for missing required arguments
        for arg_name, arg_value in required.items():
            if not arg_value:
                raise SyntaxError(f"missing required argument: '{arg_name}'\nsyntax: {self.syntax}")

        return dict(required, **optional)


commands = {}


def dos_command(attributes: dict):
    '''
    Used to decorate functions that will be used as callbacks for commands.
    Creates an instance of DOS_Command, which contains the command keyword, its arguments, and the syntax.
    :param attributes:
    :return: Decorator
    '''
    if not attributes:
        raise TypeError("attributes argument cannot be empty")
    if type(attributes) != dict:
        raise TypeError(f"attributes must be a dictionary. instead got {type(attributes)}")

    if 'keyword' not in attributes:
        raise KeyError("could not find 'keyword' in attributes")
    if 'args' not in attributes:
        raise KeyError("could not find 'args' in attributes")
    if type(attributes['args']) != list:
        raise TypeError(f"args property in attributes must be a list. instead got {type(attributes['args'])}")
    new_command = DOS_Command(attributes['keyword'])
    for arg in attributes['args']:
        new_command.add_argument(arg)
    new_command.generate_syntax()
    print('[INFO] Registered new command: ' + new_command.syntax)

    def decorator(callback):
        '''
        Used to get the function reference so it can be stored in the command instance
        :param callback:
        :return:
        '''
        new_command.callback = callback
        commands[new_command.keyword] = new_command

    return decorator


def execute_command(command: str):
    # parse the arguments
    parser = DOS_ArgumentParser()
    sections = command.split(" ", 1)
    command_keyword = sections[0]
    command_args = sections[1] if len(sections) == 2 else ''
    parsed_args = parser.parse(command_args)

    # find the relevant dos command and execute it, giving it the parsed arguments and the length of the arguments
    relevant_dos_command: DOS_Command = commands[command_keyword]
    detected_arguments = relevant_dos_command.check_syntax(parsed_args)
    if detected_arguments:
        relevant_dos_command.callback(detected_arguments, len(detected_arguments.keys()))
