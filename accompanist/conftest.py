import os

# this file is located in the root of `accompanist` package to substitute the
# `MODE` environmental variable _before_ the Settings object is created.
os.environ["MODE"] = "TEST"
