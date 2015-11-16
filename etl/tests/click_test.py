import click

@click.command()
@click.option('--act', help='what action will we perform', type = click.Choice(['cons','clean']))
@click.option('--location', help='local files or on dropbox?', type = click.Choice(['db','local']))
@click.option('--path', help='file path (pull all xls or xlsx files in it')
@click.option('--db', default=None, help='db file if consolidating')

def hello(act, location, path, db):
    if act == 'cons' and db == None:
        raise Exception('must supply a db')

if __name__ == '__main__':
    hello()