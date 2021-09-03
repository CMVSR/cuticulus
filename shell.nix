{ pkgs ? import ./nix { } }:

let
  pythonLibs = pkgs.python39.buildEnv.override {
    extraLibs = [ (import ./default.nix { inherit pkgs; }).cuticle ];
  };
in
with pkgs.python39Packages;
pkgs.mkShell {
  packages = [
    pythonLibs

    # python dev
    autopep8
    pycodestyle
    pylint
    pytest
    coverage

    # nix dev
    pkgs.nixpkgs-fmt

    # paper dev
    pkgs.texlive.combined.scheme-medium
    pkgs.jabref
    beautifulsoup4
    pkgs.pylatex
  ];
}
