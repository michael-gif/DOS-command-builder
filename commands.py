from dos import dos_command


'''
Example implementation below

@dos_command({
    'keyword': 'example',
    'args': [
        {'name': 'arg1', 'type': str, 'required': True},
        {'name': 'arg2', 'type': str, 'required': False}
    ]
})
def example(args, argc):
    print(args, argc)
'''

@dos_command({
    'keyword': 'mkdir',
    'args': [
        {'name': 'path', 'type': str, 'required': True}
    ]
})
def mkdir(args, argc):
    print("Creating directory at: " + args['path'])
