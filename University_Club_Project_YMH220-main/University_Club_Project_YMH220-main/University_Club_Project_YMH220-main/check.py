import sys
import traceback

try:
    from app.main import app
    print("Application loaded successfully.")
except Exception as e:
    print("ERROR CAUGHT:")
    print(repr(e))
    traceback.print_exc()
