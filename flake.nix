{
  description = "Ant cuticle texture analysis";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-utils = { url = "github:numtide/flake-utils"; };
    configs = { url = "github:ngngardner/configs"; };
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs { inherit system; };

      python = pkgs.python39;
      projectDir = ./.;
      overrides = pkgs.poetry2nix.overrides.withDefaults (final: prev: {
        # Python dependency overrides go here
      });

      packageName = "cuticle_analysis";
    in {
      packages.${packageName} = pkgs.poetry2nix.mkPoetryApplication {
        inherit python projectDir overrides;
        # Non-Python runtime dependencies go here
        propogatedBuildInputs = [ pkgs.opencv3];
      };

      defaultPackage = self.packages.${system}.${packageName};

      devShell = pkgs.mkShell {
        buildInputs = [
          (pkgs.poetry2nix.mkPoetryEnv {
            inherit python projectDir overrides;
          })
          pkgs.python39Packages.poetry

          # paper dev
          pkgs.texlive.combined.scheme-small
          pkgs.jabref

          # nix dev
          pkgs.nixpkgs-fmt
        ];
      };

    });
}