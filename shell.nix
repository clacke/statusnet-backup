{ pkgs ? import ./nixpkgs.nix {}
, mkShell ? pkgs.mkShell
, fetchurl ? pkgs.fetchurl
, python2 ? pkgs.python2
}:

mkShell {
  buildInputs = [(python2.withPackages (pypkgs: with pypkgs; [
    lxml
    (requests.overridePythonAttrs (oldAttrs: rec {
      name = "requests-0.14.2";
      src = fetchurl {
        url = "mirror://pypi/r/requests/${name}.tar.gz";
        sha256 = "1vxa38x0lm6l7jcn5av54abmy3052mj2glyrggqjnw8dmjl4acqf";
      };
    }))
    python-dateutil
  ]))];
}
