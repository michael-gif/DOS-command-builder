class DOS_ArgumentParser:
    def __init__(self):
        self.args = []

    def parse(self, string_args: str):
        self.args = []
        args = string_args.split(" ")
        for arg in args:
            parsed_argument = self._parse_single_argument(arg)
            self.args.append(parsed_argument)
        return self.args

    def _parse_single_argument(self, arg):
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
