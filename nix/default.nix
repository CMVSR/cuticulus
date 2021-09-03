{ sources ? import ./sources.nix }:
import sources.nixpkgs {
  overlays = [
    (_: pkgs: { inherit sources; })
    (_: pkgs: { pylatex = pkgs.callPackage ./pylatex.nix {}; })
  ];
  config = { };
}
