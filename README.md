DumbFish ♟️

DumbFish is a chess engine built from scratch in Python. It uses a custom evaluation function and alpha-beta search to select moves.

Play DumbFish

Download the Latest Release

The easiest way to run DumbFish is to download the latest executable from the **[GitHub Releases](../../releases)** page.

1. Open the [latest release](../../releases/latest).
2. Download `DumbFish-v1.0.0-macOS.zip`.
3. Extract the `.zip` file.
4. Open `DumbFish.app`.
5. Start playing!

> **macOS:** Because the application is not signed with an Apple Developer certificate, macOS may show a security warning when opening it. If this happens, right-click `DumbFish.app` and select **Open**, then confirm that you want to open it.

Run from Source

You can also run DumbFish directly from the source code.

Requirements

* Python 3
* Pygame

Install Pygame:

```bash
pip install pygame
```

Clone the repository:

```bash
git clone https://github.com/JujharSeehra/DumbFish.git
cd DumbFish
```

Run the game:

```bash
python3 Chess.py
```

Make sure the `images` folder remains in the project directory because it contains the chess piece graphics.

Features

* Custom chess engine
* Alpha-beta pruning
* Position evaluation
* Piece-square tables
* Pawn structure evaluation
* Mobility evaluation
* King safety evaluation
* King activity evaluation
* Bishop pair evaluation
* Check and checkmate detection
* Castling
* En passant
* Pawn promotion

Releases

Compiled versions of DumbFish are available on the GitHub Releases page.

The release contains a standalone executable, allowing users to play without installing Python or the project's dependencies.
