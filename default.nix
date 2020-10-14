let
  nixpkgs = builtins.fetchGit {
    name = "nixos-unstable-2020-09-26";
    url = "https://github.com/nixos/nixpkgs-channels/";
    ref = "refs/heads/nixos-unstable";
    rev = "daaa0e33505082716beb52efefe3064f0332b521";
    # obtain via `git ls-remote https://github.com/nixos/nixpkgs-channels nixos-unstable`
  };
  pkgs = import nixpkgs { config = {}; };
  pythonCore = pkgs.python38;
  pythonPkgs = python-packages: with python-packages; [
      # TODO: figure out how to keep this out of the generate Docker container
      pytest

      fastapi
      uvicorn
    ]; 
  myPython = pythonCore.withPackages pythonPkgs;
in
pkgs.stdenv.mkDerivation rec {
  name = "lmap-forever";
  src = ./.;

  installPhase = ''
    runHook preInstall
    
    mkdir -p $out/${myPython.sitePackages}
    cp -r . $out/${myPython.sitePackages}/${name}

    runHook postInstall
  '';

  propagatedbuildInputs =
    with pkgs;
    [
      git
      gnumake
      entr
      # this is only for the shell

      myPython
      # this is a requirement
    ];
  buildInputs = propagatedbuildInputs;
}
