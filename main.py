import dos

dos.debug = True


@dos.dos_command({
    'help': 'this command does something',
    'args.required': [
        {'name': 'arg1', 'type': str}
    ],
    'args.optional': [
        {'name': 'arg2', 'type': int}
    ]
})
def example_command(argv, argc):
    print(argv)
    print(argc)
    print("hello world")


dos.run_command('example a -arg2=1')
