# Observational Astronomy Course Website

[![Jupyter Book Badge](https://jupyterbook.org/badge.svg)](<http://jiaxuanli.me/ObsAstGreene/docs/index.html>)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AstroJacobLi/ObsAstGreene/HEAD)

A course designed for Princeton majors and non-majors interested in understanding astronomical data. 

Maintained by Jenny Greene, Jared Siegel, Erin Flowers, and Jiaxuan Li. 

## How to build the book?
### Creating a Conda Environment
In order to compile this book, you will need to create a conda environment with the necessary dependencies.
The conda environment is provided as `environment.yml`. This environment is used for all testing by Github Actions and can be setup by:
1. `conda env create -f environment.yml`
2. `conda activate obsastro`

### Building the Jupyter Book
After `cd` into the `ObsAstGreene` folder, run the following command in your terminal:

```bash
jb build book/
```

If you would like to work with a clean build, you can empty the build folder by running:

```bash
jb clean book/
```

If Jupyter execution is cached, this command will not delete the cached folder. 

To remove the build folder (including `cached` executables), you can run:

```bash
jb clean --all book/
```

### Publishing this Jupyter Book

This repository is published automatically to `gh-pages` upon `push` to the `master` branch.

### Notes

This repository is built based on [quantecon-mini-example](https://github.com/executablebooks/quantecon-mini-example). A more in-depth tutorial can be found [here](https://jupyterbook.org/start/overview.html).