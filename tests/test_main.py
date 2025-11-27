"""Tests for the main module."""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import main


def test_main(capsys):
    """Test the main function."""
    main()
    captured = capsys.readouterr()
    assert "Hello, World!" in captured.out
