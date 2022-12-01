from dos import dos_command


@dos_command({
    'keyword': 'mkdir',
    'args': [
        {'name': 'path', 'type': str, 'required': True},
        {'name': 'test', 'type': str, 'required': False}
    ]
})
def mkdir(args, argc):
    print(args, argc)
