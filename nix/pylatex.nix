{ sources, lib, python3Packages }:

python3Packages.buildPythonApplication rec {
  pname = "pylatex";
  version = "0.0.0";

  src = sources.PyLaTeX;

  doCheck = false;

  propagatedBuildInputs = with python3Packages; [
    ordered-set
  ];

  meta = with lib; {
    inherit (sources.pylatex) homepage description;
    license = licenses.mit;
  };
}
