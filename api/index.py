from pathlib import Path
import sys

# Make the project root importable so we can import the Flask app.
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Vercel expects a callable named `handler`.
from app import app as handler
