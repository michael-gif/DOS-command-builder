from dos import dos_command


@dos_command({
    'keyword': 'mkdir',
    'args': [
        {'name': 'path', 'type': str, 'required': True}
    ]
})
def mkdir(args, argc):
    print("Creating directory at: " + args['path'])
