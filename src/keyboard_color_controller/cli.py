import click
from .controller import Controller
from .devices import OpenRGBDevice, EmulatorDevice

@click.group()
def cli():
    """A CLI to control keyboard lighting."""
    pass

@cli.command()
@click.option('--color', default='red', help='Color to set the keyboard to.')
@click.option('--emulator', is_flag=True, help='Use the emulator.')
def set_color(color, emulator):
    """Sets the entire keyboard to a single color."""
    if emulator:
        device = EmulatorDevice()
        controller = Controller(device)
        controller.set_color(color)
        click.echo(f"Setting keyboard color to {color}")
        device.process.join()
    else:
        device = OpenRGBDevice()
        controller = Controller(device)
        controller.set_color(color)
        click.echo(f"Setting keyboard color to {color}")

if __name__ == '__main__':
    cli()
