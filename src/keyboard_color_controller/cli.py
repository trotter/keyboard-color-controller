import click

@click.group()
def cli():
    """A CLI to control keyboard lighting."""
    pass

@cli.command()
@click.option('--color', default='red', help='Color to set the keyboard to.')
def set_color(color):
    """Sets the entire keyboard to a single color."""
    click.echo(f"Setting keyboard color to {color}")

if __name__ == '__main__':
    cli()
