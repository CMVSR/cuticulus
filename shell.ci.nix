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
    pytest
    coverage
  ];
}
