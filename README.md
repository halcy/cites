# cites

Basic bibtex to static site generator so you can easily self-archive and help kill
the academic publishing industry.

## Sample

https://halcy.de/cites/

## Features

* Self-contained
* Works directly from bibtex file
* Included PDF reader
* Can add links to poster, talk recording video, ...
* Abstract display
* Mathjax to render math correctly
* Search function on the list page
* Relatively easy to use (I think)
* Looks cool, relatively easy to customize.

## Usage

1) Clone this repo to somewhere publicly accessible on your web server. Install python and jinja2 using a method of your choice.
2) Create a bibtex file with your references. See included for example.
3) Drop appropriately named pdf files into the "pdf" folder (and get rid of the ones I put in there as a sample)
4) Run genbib.py. Adjust defaults in the file as needed, or pass arguments.

You now have an "index.html" in this folder, and a bunch of paper pages in the "papers" folder, which looks like so:

![screenshot of https://halcy.de/cites/](https://github.com/halcy/cites/blob/main/screenshot.png?raw=true)

# Things that would be cool

I would love to be able to just have the paper content as html, but that'd require a lot of work (even assuming you start from Tex source rather than PDF). So if you, reader, have some cool patch that does this, I would love to merge it.

# Acknowledgements

The layout of this list is heavily inspired by https://github.com/monperrus/bibtexbrowser , though it is a complete from scratch remake.
