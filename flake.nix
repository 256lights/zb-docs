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

        woosh = pkgs.callPackage ./woosh.nix {};
      in
      {
        packages.woosh = woosh;

        devShells.default = pkgs.mkShell {
          packages = [
            python
            pkgs.netlify-cli
            pkgs.texliveFull
            woosh
          ];
        };
      }
    );
}
