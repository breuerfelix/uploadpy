{ pkgs ? import <nixpkgs> {} }:
let
  highzer = pkgs.poetry2nix.mkPoetryEnv {
    projectDir = ./.;
    editablePackageSources = {
      uploadpy = ./uploadpy;
    };
  };
in highzer.env.overrideAttrs (oldAttrs: {
  buildInputs = with pkgs; [
    python3
    poetry
    geckodriver
  ];
})
