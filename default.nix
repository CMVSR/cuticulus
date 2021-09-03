{ sources ? import ./nix/sources.nix
, pkgs ? import ./nix { inherit sources; }
}:
with pkgs;
rec {
  cuticle = python39Packages.buildPythonPackage {
    pname = "cuticle_analysis";
    version = "0.0.1";

    src = lib.cleanSourceWith {
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
      src = lib.cleanSource ./.;
    };

    propagatedBuildInputs = with python39Packages; [
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
}
