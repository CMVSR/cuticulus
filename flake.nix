{
  description = "Ant cuticle texture analysis";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/d189bf92f9be23f9b0f6c444f6ae29351bb7125c";
    utils = { url = "github:numtide/flake-utils"; };
    configs = { url = "github:ngngardner/configs"; };
    gitignore = {
      url = "github:hercules-ci/gitignore.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, utils, configs, gitignore }:
    {
      overlay = final: prev: {
        cuticle = final.callPackage ./default.nix { };
        inherit (gitignore.lib) gitignoreSource;
      };
    } //
    (utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [
            configs.overlay
            self.overlay
          ];
        };
      in
      {
        defaultPackage = pkgs.callPackage ./default.nix { };

        devShell = pkgs.mkShell {
          packages = [
            pkgs.cuticle

            # python dev
            pkgs.python39Packages.autopep8
            pkgs.python39Packages.pycodestyle
            pkgs.python39Packages.pylint
            pkgs.python39Packages.pytest
            pkgs.python39Packages.coverage

            # gui
            pkgs.python39Packages.pygame

            # paper dev
            (pkgs.texlive.combine {
              inherit (pkgs.texlive) scheme-small;
            })
            pkgs.pylatex
          ];
        };
      })
    );
}
