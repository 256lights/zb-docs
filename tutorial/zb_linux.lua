local zb <const> = fetchArchive {
  url = "https://github.com/256lights/zb-stdlib/releases/download/v0.1.1/zb-stdlib-v0.1.1.tar.gz";
  hash = "sha256:ee4c78f4b1915c7dafb0d55e8cd6f20fe82396a21a6ab2add9bb879fb9301bc2";
}
local stdenv = import(zb.."/stdenv/stdenv.lua")

sqlite3 = stdenv.makeDerivation {
  pname = "sqlite3";
  version = "3.50.1";
  src = fetchurl {
    url = "https://www.sqlite.org/2025/sqlite-autoconf-3500100.tar.gz";
    hash = "sha256:00a65114d697cfaa8fe0630281d76fd1b77afcd95cd5e40ec6a02cbbadbfea71";
  };

  buildSystem = "x86_64-unknown-linux";
  configureFlags = "--enable-static --disable-shared";
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

  buildSystem = "x86_64-unknown-linux";

  C_INCLUDE_PATH = strings.makeIncludePath {
    sqlite3
  };
  LIBRARY_PATH = strings.makeLibraryPath {
    sqlite3
  };

  buildPhase = "gcc -o hello-sql hello_sql.c -l:libsqlite3.a";
  installPhase = '\z
    mkdir -p "$out/bin"\n\z
    mv hello-sql "$out/bin/hello-sql"\n';
}
