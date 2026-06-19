{ buildGoModule
, fetchFromGitHub
, lib
}:

let
  commit = "7dafeacc239d9379afa062b6e4a0e0bcfefc26c1";
in

buildGoModule {
  pname = "woosh";
  version = commit;

  src = fetchFromGitHub {
    owner = "zombiezen";
    repo = "woosh";
    rev = commit;
    hash = "sha256-5NrcKOjbCie3sSuRT3C4zPiPCZA6e+bKB7PLR6euUwE=";
  };

  ldflags = [ "-s -w" ];

  vendorHash = "sha256-KXc+pMWarbg5E0neky+h/yztmzIIx+GmigzsUdj2194=";

  meta = {
    description = "A CSS preprocessor that supports utility classes with optional suffixes generated based on usage.";
    homepage = "https://github.com/zombiezen/woosh";
    license = lib.licenses.mit;
  };
}
