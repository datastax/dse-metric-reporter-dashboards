#!/usr/bin/env python

import os

with open("VERSION.txt", "r") as f:
    version = f.read()

    os.chdir("dist")
    os.system(f"zip -r -9 dse-metrics-reporter-dashboards-{version}.zip .")
