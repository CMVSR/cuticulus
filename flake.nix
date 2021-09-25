{
  description = "Ant cuticle texture analysis";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-utils = { url = "github:numtide/flake-utils"; };
    configs = { url = "github:ngngardner/configs"; };
  };

  outputs = { self, nixpkgs, flake-utils, configs }:
    flake-utils.lib.eachDefaultSystem
      (system:
        let
          pkgs = import nixpkgs {
            inherit system;
            overlays = [
              configs.overlay
            ];
          };
        in
        {
          defaultPackage = pkgs.callPackage ./default.nix { };
          devShell = import ./shell.nix { inherit pkgs; };
        });
}
