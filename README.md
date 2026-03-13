# Retro Games
A collection of classic arcade games developed in Python. The software includes an 80s-style arcade cabinet menu to select and launch the available games.

---
## Included Games
* **Pac-Man**: Classic maze game.
* **Snake**: The famous snake game.
---

## Installation and Execution

You can download the latest stable version directly from the [Releases](https://github.com/MichelaTasca/Retro_Games/releases/tag/v1.0.3) section.
Pre-compiled executables are available for:
* **Windows**: `RetroGames-Windows.exe`
* **macOS**: `RetroGames-macOS`
* **Linux**: `RetroGames-Linux`

---
## Menu Controls
* UP/DOWN Arrow: Navigate through the available games.
* ENTER: Confirm the selection and start the game.
---
## Development Setup
If you want to run the project from source or contribute:

### Requirements
* **Python 3.12+** (CI pipeline is optimized for Python 3.14)
* `pip` package manager

### Installation and Execution
1. Clone this repository and navigate to the project's root directory.
2. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Linux/macOS: source venv/bin/activate | On Windows: venv\Scripts\activate
   ```
3. Install the runtime dependencies:
```bash
   pip install -r requirements.txt
```
4. Run the application
```bash
   python main.py
```

---
## Development and Testing
If you want to contribute or run the test suite, you must install the development dependencies:
   ```bash
   pip install -r requirements_dev.txt
   ```
The project uses `pytest` for testing. To run the tests with coverage analysis, use the following command:
   ```bash
   pytest --cov-config=.coveragec --cov=src --cov=main 
   ```
The project utilizes a Continuous Integration (CI) system that automatically performs:

* **Unit Testing**: powered by `pytest` with code coverage analysis.
* **Static Analysis**: code is verified using `pylint`, `mypy`,`flake8`, `black`, and `isort` to ensure high quality standards.
* **Automated Build**: every release is compiled for Windows, macOS, and Linux via GitHub Actions and PyInstaller.