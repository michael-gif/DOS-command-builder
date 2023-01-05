# DOS-Command-builder-parser
Will allow you to build dos commands with decorator syntax, and does syntax checking for you

## Features
- Argument parsing (using argparse)
- Lightweight
- Fast
- Easy to use

## Example
```python
import dos

dos.debug = True


@dos.dos_command({
    'keyword': 'example',
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
```

## Notes
- `dos.debug` is set to `False` by default. Set it to `True` if you want to see when the commands are registered.
- `keyword` is optional in the decorator. If you don't specify a keyword, then the name of the function will be used instead.  
In the example above, if `'example'` wasn't specified, then `'example_command'` would have been used instead.
