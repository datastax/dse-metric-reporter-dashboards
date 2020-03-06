#!/usr/bin/env python

import shutil
import os

if os.path.isdir("generated"):
    shutil.rmtree("generated")
