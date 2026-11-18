import os
import sys
import runpy

# Forward to engine/scripts/specialist-manager.py
script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts", "specialist-manager.py")
if os.path.exists(script_path):
    sys.argv[0] = script_path
    runpy.run_path(script_path, run_name="__main__")
else:
    print(f"Error: Could not find {script_path}", file=sys.stderr)
    sys.exit(1)
