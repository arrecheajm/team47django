{pkgs}: {
  deps = [
    pkgs.imagemagick_light
    pkgs.jq.bin
    pkgs.apacheHttpd
    pkgs.zlib
    pkgs.xcodebuild
    pkgs.vim-full
    pkgs.sqlite.bin
    pkgs.glibcLocales
  ];
}
