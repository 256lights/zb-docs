-- zb.lua

-- Download the standard library.
local zb <const> = fetchArchive {
  url = "https://github.com/256lights/zb-stdlib/releases/download/v0.1.1/zb-stdlib-v0.1.1.tar.gz";
  hash = "sha256:ee4c78f4b1915c7dafb0d55e8cd6f20fe82396a21a6ab2add9bb879fb9301bc2";
}

-- Import modules from the standard library.
local stdenv = import(zb.."/stdenv/stdenv.lua")

-- Copy the source to the store.
local src = path {
  path = ".";
  name = "hello-source";
  filter = function(name)
    return name == "hello.c"
  end;
}

-- Create our build target.
-- Replace with your system, if necessary.
-- One of:
-- x86_64-unknown-linux
-- aarch64-apple-macos
local buildSystem <const> = "x86_64-unknown-linux"

hello = stdenv.makeDerivation {
  pname = "hello";
  src = src;

  buildSystem = buildSystem;

  buildPhase = "gcc -o hello hello.c";
  installPhase = '\z
    mkdir -p "$out/bin"\n\z
    mv hello "$out/bin/hello"\n';
};

sqlite3 = stdenv.makeDerivation {
  pname = "sqlite3";
  version = "3.50.1";
  src = fetchurl {
    url = "https://www.sqlite.org/2025/sqlite-autoconf-3500100.tar.gz";
    hash = "sha256:00a65114d697cfaa8fe0630281d76fd1b77afcd95cd5e40ec6a02cbbadbfea71";
  };

  buildSystem = "aarch64-apple-macos";
}

-- Dependencies:
local strings = import(zb.."/strings.lua")

hello_sql = stdenv.makeDerivation {
  pname = "hello-sql";
  src = path {
    path = ".";
    name = "hello-sql-source";
    filter = function(name)
      return name == "hello_sql.c"
    end;
  };

  buildSystem = "aarch64-apple-macos";

  C_INCLUDE_PATH = strings.makeIncludePath {
    sqlite3
  };
  LIBRARY_PATH = strings.makeLibraryPath {
    sqlite3
  };

  buildPhase = "gcc -o hello-sql -lsqlite3 hello_sql.c";
  installPhase = '\z
    mkdir -p "$out/bin"\n\z
    mv hello-sql "$out/bin/hello-sql"\n';
}
