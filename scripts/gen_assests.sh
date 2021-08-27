#!/bin/bash

nix-shell --run "
cuticle_analysis --download-dataset \
&& python scripts/data_spread.py
"
