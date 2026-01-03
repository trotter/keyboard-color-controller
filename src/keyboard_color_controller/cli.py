import click
from typing import Tuple, List, TextIO
from .controller import Controller
from .devices import OpenRGBDevice, EmulatorDevice, Device

@click.group()
def cli() -> None:
    """A CLI to control keyboard lighting."""
    pass

def get_device(emulator: bool) -> Device:
    return EmulatorDevice() if emulator else OpenRGBDevice()

@cli.command()
@click.option('--color', default='red', help='Color to set the keyboard to (name or #RRGGBB).')
@click.option('--emulator', is_flag=True, help='Use the emulator.')
def set_color(color: str, emulator: bool) -> None:
    """Sets the entire keyboard to a single color."""
    device = get_device(emulator)
    controller = Controller(device)
    controller.set_color(color)
    click.echo(f"Setting keyboard color to {color}")
    if emulator and isinstance(device, EmulatorDevice):
        device.process.join()

@cli.command()
@click.option('--key', multiple=True, help='Key to set the color for (can be specified multiple times).')
@click.option('--color', default='red', help='Color to set the key(s) to (name or #RRGGBB).')
@click.option('--emulator', is_flag=True, help='Use the emulator.')
def set_key(key: Tuple[str, ...], color: str, emulator: bool) -> None:
    """Sets the color of specific key(s)."""
    if not key:
        click.echo("Please specify at least one key using --key option.")
        return

    device = get_device(emulator)
    controller = Controller(device)
    for k in key:
        controller.set_key_color(k, color)
    click.echo(f"Setting key(s) {', '.join(key)} to {color}")

    if emulator and isinstance(device, EmulatorDevice):
        device.process.join()

@cli.command()
@click.argument('art_file', type=click.File('r'))
@click.option('--fg', default='red', help='Foreground color.')
@click.option('--bg', default='black', help='Background color.')
@click.option('--emulator', is_flag=True, help='Use the emulator.')
def ascii_art(art_file: TextIO, fg: str, bg: str, emulator: bool) -> None:
    """Displays ASCII art on the keyboard from a file."""
    art = art_file.read()
    device = get_device(emulator)
    controller = Controller(device)
    controller.set_ascii_art(art, fg, bg)
    click.echo(f"Displaying ASCII art from {art_file.name}")
    if emulator and isinstance(device, EmulatorDevice):
        device.process.join()

if __name__ == '__main__':
    cli()
