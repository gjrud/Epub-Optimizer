# Epub Optimizer

A Sysadmin's idea of "coding".

## Description

This script extracts one or more EPUBs in the output directory, compresses all images using pillow at quality 75 and then creates new EPUBs using the compressed images.
At the end all folders created during extraction are deleted for cleanup.

This Script was made to help me more easily archive the various LN in EPUB format that i own.

## Usage

    epuboptimizer [-h] [--debug DEBUG] --input INPUT --output OUTPUT

| OPTION | IS REQUIRED | DESCRIPTION |
|--------|-------------|-------------|
| -h | no | Show help message and exit |
| --debug DEBUG | no | print debug messages true/false (default: false) |
| --input INPUT | yes | Path to input file or folder |
| --output OUTPUT | yes | Path to output folder |
