{ lib, python39Packages, gitignoreSource }:



python39Packages.buildPythonPackage
{
  pname = "cuticle_analysis";
  version = "0.0.1";

  src = gitignoreSource ./.;

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
}
