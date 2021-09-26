{
  description = "Ant cuticle texture analysis";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-utils = { url = "github:numtide/flake-utils"; };
    configs = { url = "github:ngngardner/configs"; };
  };

  outputs = { self, nixpkgs, flake-utils, configs }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { 
          inherit system; 
          overlays = [
            configs.overlay
          ];
        };

        cuticle = pkgs.python39Packages.buildPythonPackage {
          pname = "cuticle_analysis";
          version = "0.0.1";

          src = pkgs.lib.cleanSourceWith {
            filter = (path: type:
              ! (builtins.any
                (r: (builtins.match r (builtins.baseNameOf path)) != null)
                [
                  "dataset"
                  "logs"
                  "result"
                  "pip_packages"
                  "scripts"
                  "gui"
                  "paper"
                  ".*\.egg-info"
                  ".*\.zip"
                ])
            );
            src = pkgs.lib.cleanSource ./.;
          };

          propagatedBuildInputs = with pkgs.python39Packages; [
            colorama
            gdown
            matplotlib
            numpy
            opencv3
            openpyxl
            pandas
            pillow
            python-dotenv
            requests
            scikit-learn
            scipy
            tensorflow
            questionary
          ];

          doCheck = false;
          pythonImportsCheck = [ "cuticle_analysis" ];
        };
      in
      {
        packages.cuticle = cuticle;
        defaultPackage = cuticle;

        devShell = pkgs.mkShell {
          packages = [
            cuticle

            # python dev
            pkgs.python39Packages.autopep8
            pkgs.python39Packages.pycodestyle
            pkgs.python39Packages.pylint
            pkgs.python39Packages.pytest
            pkgs.python39Packages.coverage

            # nix dev
            pkgs.nixpkgs-fmt

            # paper dev
            pkgs.texlive.combined.scheme-small
            pkgs.jabref
            pkgs.pylatex
          ];
        };
      });
}
