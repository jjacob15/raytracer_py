import sys
import os
curr_dir = os.path.dirname(__file__)
print(os.path.join(curr_dir, f"..{os.path.pathsep}", "raytracer"))
# sys.path.append(curr_dir + "..")
