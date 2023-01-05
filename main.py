from dos import dos_command, run_command

@dos_command({
    'keyword': 'example',
    'help': 'this command does something',
    'args.required': [
        {'name': 'arg1', 'type': str},
        {'name': 'arg2', 'type': str}
    ],
    'args.optional': [
    ]
})
def test(argv, argc):
    print(argv)
    print("hello world")

run_command('example a b')