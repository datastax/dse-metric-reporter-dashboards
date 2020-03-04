#!/usr/bin/env python

import shutil
import os

if os.path.isdir("dist"):
    shutil.rmtree("dist")
