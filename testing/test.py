#!/usr/bin/env python3
import subprocess


cmd = [
    "bash", "test.sh"
]

subprocess.run(cmd, env={})
