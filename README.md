# cuticulus

This repository is for the project "Ant Cuticle Texture Analysis".

## Installation

### Requirements

1. [git](https://git-scm.com/downloads)
2. [nix](https://nixos.org/) (option #1)
3. [poetry](https://python-poetry.org/) (option #2)
4. [conda](https://conda.io/) (optional)

This project utilizes [nix](https://nixos.org/) for building and running.

```
$ git clone https://github.com/ngngardner/cuticle_analysis
$ cd cuticulus
$ nix-shell --run "cuticulus" # install dataset
```

Alternatively, install dependencies with [poetry](https://python-poetry.org/):

```
$ git clone https://github.com/ngngardner/cuticle_analysis
$ cd cuticulus
$ conda env create -f environment.yaml # get correct python version
$ conda activate cuticulus
$ poetry install
$ cuticulus
```
