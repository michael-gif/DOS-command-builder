import dos

dos.debug = True


@dos.dos_command({
    'keyword': 'test',
    'help': 'this command does something',
    'args.required': [
        {'name': 'arg1', 'type': str},
    ],
    'args.optional': [
        {'name': 'arg2', 'type': int}
    ]
})
def example_command(argv, argc):
    print(argv)
    print(argc)
    print("hello world")
    return 69


print(dos.run_command('test 1 2'))
