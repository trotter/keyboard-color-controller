# Keyboard Color Controller

A Python-based CLI tool to control RGB lighting on keyboards using OpenRGB or a built-in emulator.

## Features

- Set the entire keyboard to a single color.
- Set individual keys to specific colors.
- Display ASCII art on the keyboard.
- Includes a GUI emulator for testing without physical hardware.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/trotter/keyboard-color-controller.git
   cd keyboard-color-controller
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

## Usage

You can run the controller using the `keyboard_color_controller` module. Ensure the `src` directory is in your `PYTHONPATH`:

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python3 -m keyboard_color_controller --help
```

### Commands

#### Set Entire Keyboard Color
Sets every key to the specified color.

```bash
python3 -m keyboard_color_controller set-color --color blue
```

To use the emulator:
```bash
python3 -m keyboard_color_controller set-color --color blue --emulator
```

#### Set Specific Keys
Sets one or more keys to a specific color.

```bash
python3 -m keyboard_color_controller set-key --key "Esc" --key "F1" --color green
```

#### Display ASCII Art
Displays ASCII art from a file on the keyboard layout.

```bash
python3 -m keyboard_color_controller ascii-art art.txt --fg red --bg black
```

### Key Names
Refer to `src/keyboard_color_controller/layout.py` for valid key names.

## Development

### Running Tests
To run the unit tests:

```bash
PYTHONPATH=src python3 -m unittest discover tests
```

## License
MIT License. See [LICENSE](LICENSE) for details.
