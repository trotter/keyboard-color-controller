import click
from .controller import Controller
from .devices import OpenRGBDevice, EmulatorDevice
import time

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
    else:
        device = OpenRGBDevice()

    controller = Controller(device)
    controller.set_color(color)
    click.echo(f"Setting keyboard color to {color}")
    # Give the emulator time to start and process the command
    if emulator:
        time.sleep(2)

if __name__ == '__main__':
    cli()