# Python Project

A Python project with a clean, standard structure.

## Project Structure

```
bot/
├── src/              # Source code
├── tests/            # Test files
├── requirements.txt  # Project dependencies
├── setup.py         # Package configuration
└── README.md        # This file
```

## Getting Started

### Prerequisites

- Python 3.8 or higher

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

```bash
python -m src.main
```

### Running Tests

```bash
pytest tests/
```

## Development

To install the project in editable mode for development:

```bash
pip install -e .
```

## License

This project is licensed under the MIT License.
