# Cellular Automata Simulator

## Description
This app allows the user to simulate a 100x100 grid of a cellular automata, more specifically Conway's Game of Life. The simulator starts in a random configuration, although the grid can be cleaned up at any moment and custom patterns can be drawn by directly clicking the cells in the grid. Additionally, some interesting patterns can be accessed through the Patterns menu.

Althoug the grid is closed by default, the boundaries can be opened so that the grid loops around.

## Controls
- Left/Right/Up/Down: scroll through the grid in a given direction.
- R: Rotate the selected pattern clockwise
- F: Flip the selected pattern horizontally.
- Mouse scroll up/down: Zoom in/out.


## Usage
The application is bundled as an executable file, which can be found in the dist folder. The application can be run by simply double-clicking on the executable. To run the python implementation the following command must be entered in a terminal inside the folder with the scripts:

```python3 main.py```

The code was developed using PyGame 2.5.2 and Python 3.10.9.
