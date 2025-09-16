{
  description = "Ma";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";

  outputs = { self, nixpkgs }:
  let
    forAllSystems = f:
      nixpkgs.lib.genAttrs [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ] (system:
        f system (import nixpkgs { inherit system; config = {}; overlays = []; }));
  in
  {
    devShells = forAllSystems (system: pkgs: {
      default = pkgs.mkShell {
        packages = with pkgs; [
          python312
          ffmpeg
          libopus
          libsodium
        ];
        LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [ pkgs.libopus pkgs.libsodium ];
      };
    });
  };
}