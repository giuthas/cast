# CAST Development guide

For lack of actual content here (apart from the installing instructions below),
look up the corresponding guide from SATKIT.

## Install CAST in development mode 

This is an untested recipe generated from a vague memory of a confusing process
of getting things to work. If you do start testing and need help and/or have
corrections, please get in touch.

- Get the repository: e.g. after forking on GitHub 
  `git clone [your repo url] [directory name you like]`
- After which the run following in the repository root
- Get [pixi](https://pixi.sh/) `pip install pixi`
- Get [hatch](https://hatch.pypa.io/) `pip install hatch`
- Build the environments `pixi build` and _probably_ switch to the devel one
- Build the package `hatch build`
- And finally install it in editable mode `pip install -e .` 
  (The final '.' matters.)