{
  description = "Python script to manage latex lectures with neovim and rofi";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {inherit system;};
      lib = pkgs.lib;

      python = pkgs.python3;

      # Pacchetto Python con la tua libreria (che ora è in lib/unilib)
      unilib = pkgs.python3Packages.buildPythonPackage {
        pname = "unilib";
        version = "0.1.0";
        src = ./lib;
        format = "setuptools";
        nativeBuildInputs = [pkgs.python3Packages.setuptools];
      };

      # Ambiente Python con eventuali pacchetti aggiuntivi
      pythonEnv = python.withPackages (ps:
        with ps; [
          # eventuali pacchetti, es: click, requests, ecc.
          pyyaml
        ]);

      # Genera uno script binario per ogni file in scripts/
      mkScript = name: {
        type = "app";
        program = "${pkgs.writeShellScriptBin name ''
          export PYTHONPATH=${unilib}/${python.sitePackages}
          exec ${pythonEnv}/bin/python ${./scripts}/${name}.py "$@"
        ''}/bin/${name}";
      };

      scriptFiles = builtins.attrNames (builtins.readDir ./scripts);
      scriptApps = builtins.listToAttrs (map (s: {
        name = lib.removeSuffix ".py" s;
        value = mkScript (lib.removeSuffix ".py" s);
      }) (lib.filter (s: builtins.match ".*\\.py$" s != null) scriptFiles));
    in {
      packages.default = pkgs.stdenv.mkDerivation {
        pname = "uni-scripts";
        version = "0.1.0";
        src = ./scripts;
        buildInputs = [pythonEnv];
        installPhase = ''
              mkdir -p $out/bin
              for f in *.py; do
                name=$(basename "$f" .py)
                cat > $out/bin/$name <<EOF
          #!/usr/bin/env bash
          export PYTHONPATH=${unilib}/${python.sitePackages}
          exec ${pythonEnv}/bin/python $out/scripts/$f "\$@"
          EOF
              chmod +x $out/bin/$name
              done
              mkdir -p $out/scripts
              cp *.py $out/scripts/
        '';
      };
      apps = scriptApps;

      devShells.default = pkgs.mkShell {
        buildInputs = [pythonEnv unilib];
        shellHook = ''
          echo "✔ Ambiente pronto. PYTHONPATH settato a unilib."
        '';
      };
    });
}
