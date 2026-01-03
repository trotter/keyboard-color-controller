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

@cli.command()
@click.option('--key', multiple=True, help='Key to set the color for (can be specified multiple times).')
@click.option('--color', default='red', help='Color to set the key(s) to.')
@click.option('--emulator', is_flag=True, help='Use the emulator.')
def set_key(key, color, emulator):
    """Sets the color of specific key(s)."""
    if not key:
        click.echo("Please specify at least one key using --key option.")
        return

    device = EmulatorDevice() if emulator else OpenRGBDevice()

    controller = Controller(device)
    for k in key:
        controller.set_key_color(k, color)
    click.echo(f"Setting key(s) {', '.join(key)} to {color}")

    if emulator:
        device.process.join()

@cli.command()
@click.argument('art_file', type=click.File('r'))
@click.option('--fg', default='red', help='Foreground color.')
@click.option('--bg', default='black', help='Background color.')
@click.option('--emulator', is_flag=True, help='Use the emulator.')
def ascii_art(art_file, fg, bg, emulator):
    """Displays ASCII art on the keyboard from a file."""
    art = art_file.read()
    device = EmulatorDevice() if emulator else OpenRGBDevice()
    controller = Controller(device)
    controller.set_ascii_art(art, fg, bg)
    click.echo(f"Displaying ASCII art from {art_file.name}")
    if emulator:
        device.process.join()

if __name__ == '__main__':
    cli()
