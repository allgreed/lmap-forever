let
  pkgs = import <nixpkgs> {};
  app = import ./default.nix;
in
pkgs.dockerTools.buildImage {
  name = "lmap-forever";
  tag = "builded";

  #created = "now";

  contents = app;

  config = {
    Cmd = [
      # TODO: unhardcode python3.8
      # TODO: unhardcode app name
      "${app}/lib/python3.8/site-packages/lmap-forever/src/main.py"
    ];

    ExposedPorts = {
      "12694/tcp" = {};
    };

    Env = [
      # TODO: unhardcode python3.8
      # TODO: unhardcode app name
      "PYTHONPATH=${app}/lib/python3.8/site-packages/lmap-forever/"
    ];
  };
}
