# lmap-forever
Backing service for lmap, designed for running locally and storing the state

## Installation

### Home-manager
The recommended installation methid is using [home-manager](TODO), simply copy the following into your `home.nix` and modify the values between `{` and `}`:
```nix
  systemd.user.services = {
    lmap-forever = {
      Unit = {
        Description = "lmap-forever";
        Documentation = [
          "https://github.com/allgreed/lmap-forever"
          "https://github.com/allgreed/lmap"
        ];
      };

      Install = {
        WantedBy = [ "multi-user.target" ];
      };

      Service = {
        TimeoutStartSec = 0;
        Restart = "always";
        ExecStartPre="/bin/sh -c 'export PATH=/run/current-system/sw/bin/:/usr/bin/; docker stop lmap-forever && (docker rm lmap-forever || true) || true'";
        ExecStart="/bin/sh -c 'export PATH=/run/current-system/sw/bin/:/usr/bin/; docker run -e STORAGE_PROVIDER_TYPE=file -e STORAGE_PROVIDER_FILE_PATH=/data -v /home/{your_username}/lmap:/data --rm --name lmap-forever -p 12694:12694 allgreed/lmap-forever:{tag_of_your_choice}'";
      };
    };
  };
```

### Docker
but of course you can use it simply via Docker as well:
```bash
docker run -e STORAGE_PROVIDER_TYPE=file -e STORAGE_PROVIDER_FILE_PATH=/data -v /home/{your-username}/lmap:/data --restart=always --name lmap-forever -p 12694:12694 allgreed/lmap-forever:{tag_of_your_choice}
```

### Note on tags
The list of tags can be found [here](https://hub.docker.com/r/allgreed/lmap-forever/tags)
TODO: setup CI and change the default tag to latest

## Note on ports
By default port 12694 is utilized, not the most memorable one, but it's not reserved by IANA or anything

## Dev

### Prerequisites
- [nix](https://nixos.org/nix/manual/#chap-installation)
- `direnv` (`nix-env -iA nixpkgs.direnv`)
- [configured direnv shell hook ](https://direnv.net/docs/hook.html)
- some form of `make` (`nix-env -iA nixpkgs.gnumake`)

Hint: if something doesn't work because of missing package please add the package to `default.nix` instead of installing on your computer. Why solve the problem for one if you can solve the problem for all? ;)

### One-time setup
```
make init
```

### Everything
```
make help
```
