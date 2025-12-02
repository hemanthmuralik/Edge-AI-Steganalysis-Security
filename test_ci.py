import sys
import os

# Explicitly add the current directory to the system path
sys.path.append(os.getcwd())

print("Attempting to import Ye-Net...")

try:
    from models.ye_net import build_yenet
    print("Import successful!")
    
    model = build_yenet()
    model.summary()
    print("✅ Ye-Net Architecture Verified Successfully")
    
except ImportError as e:
    print(f"❌ ImportError: {e}")
    # Print the file structure to debug
    print("\n--- Debugging File Structure ---")
    for root, dirs, files in os.walk("."):
        for filename in files:
            print(os.path.join(root, filename))
    sys.exit(1)
except Exception as e:
    print(f"❌ Runtime Error: {e}")
    sys.exit(1)
