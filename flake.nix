{
  inputs = {
    nixpkgs.url = "nixpkgs";
    flake-utils.url = "flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };

        python = pkgs.python3.withPackages (ps: [
          ps.myst-parser
          ps.sphinx
          ps.sphinx-reredirects
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            python
            pkgs.texliveFull
          ];
        };
      }
    );
}
