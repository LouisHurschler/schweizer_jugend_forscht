{
  description = "flake template";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
        # config.allowUnfree = true;
      };
      
    in
    {
      formatter.${system} = pkgs.nixpkgs-fmt;

      devShell.${system} = pkgs.mkShell rec {
        nativeBuildInputs = with pkgs; [
        mosquitto
        lsof
        tcpdump
        dnsmasq
        hostapd
        iw

        (python3.withPackages (ps: with ps;
                  [
                    python-lsp-server
                    ipython
                    black

                    matplotlib
                    numpy
                    pandas
                    tkinter
                    plotly
                    paho-mqtt
                    google
                    protobuf
                  ]))        ];
        buildInputs = with pkgs; [ 
        ];

        CPATH = pkgs.lib.makeSearchPathOutput "dev" "include" buildInputs;
        LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath buildInputs;
      };
    };
}
