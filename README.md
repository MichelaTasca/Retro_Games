# Retro Games
A collection of classic arcade games developed in Python. The software includes an 80s-style arcade cabinet menu to select and launch the available games.
---
## Included Games
* **Pac-Man**: Classic maze game.
* **Snake**: The famous snake game.
---
## Requirements
* Python 3.x (The CI pipeline is configured for Python 3.14)
* `pip` package manager

## Installation and Execution

1. Clone this repository and navigate to the project's root directory.
2. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Linux/macOS:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```
3. Install the base runtime dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```
---
## Menu Controls
* UP/DOWN Arrow: Navigate through the available games.
* ENTER: Confirm the selection and start the game.
---
## Development and Testing
If you want to contribute or run the test suite, you must install the development dependencies:
   ```bash
   pip install -r requirements_dev.txt
   ```
The project uses `pytest` for testing. To run the tests with coverage analysis, use the following command:
   ```bash
   pytest --cov=src --cov=main tests/
   ```
Code quality and formatting are maintained using `pylint`, `flake8`, `mypy`, `black`, and `isort`.