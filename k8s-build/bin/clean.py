#!/usr/bin/env python

import shutil
import os

base_path = os.path.join(os.path.dirname(__file__), "..")
generated_path = os.path.join(base_path, "generated")

if os.path.isdir(generated_path):
    print(f"Removing {generated_path}")
    shutil.rmtree(generated_path)
