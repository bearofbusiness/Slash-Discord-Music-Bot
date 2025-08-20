let
  pkgs = import <nixpkgs> {};
in
pkgs.mkShell {
  packages = with pkgs; [
    python312
    ffmpeg
    libopus
    libsodium
  ];

  LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [ pkgs.libopus pkgs.libsodium ];
}
