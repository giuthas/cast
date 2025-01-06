
# CAST

Computer Assisted Segmentation Tools (CAST) is a helper toolkit for phonetic
analysis. Based on config files and metadata it generates a dumb segmentation
that can then be adjusted in Praat or other TextGrid editing programs.

CAST *does not* do forced alignment. There is no acoustic (nor articulatory)
analysis of speech under the hood, only some adjustable heuristics for selecting
a reasonable guess for where the speech is for the utterance and word levels and
then a totally rule-based segmentation based on a pronunciation dictionary.

CAST *does* provide a segmentation template that is meant to be easy for a human
annotator to adjust. For this reason all automatically generated segments are of
equal length within a given word.

CAST *does* do the writing and boundary creation for you. No need to go back and
correct typos in the transcription -- at least on the phonological level -- and
a good deal less carpal tunnel strain because of reduced number of mouse clicks.
And a significantly more relaxed feel about the segmentation process in general.

CAST *is* aware that data beyond simple audio exist and will include features in
the future that take this into account.

## Current version is 0.1.0

See [Changelog](docs/Changelog.md) for what is new.

## Roadmap to 1.0

CAST is going to be re-organised a bit in the very near future (during 
2025 if nothing weird happens). Version 1.0 will include:

- At least four commandline commands:
  - `add` which add Tiers to TextGrids up to the specified level (see below).
    `add` will also generate the TextGrids if they do not already exist.
    - The Tier levels will be L0=[File], L1=[Utterance], L2=Word, L3=Phonemes,
      L4=Phones. Levels whose names are in brackets can be turned off as a
      configuration option. All preceding levels (that haven't been turned off)
      above the requested level will be added to the TextGrid. The File level is
      turned off by default when not running `concatenate`. All levels maybe
      renamed as a configuration option.
  - `concatenate` produces a concatenated wav file and corresponding TextGrid
    for working on multiple recordings in Praat.
  - `extract` extracts TextGrids corresponding to individual recordings from a
    previously concatenated set of recordings.
  - `remove-double-word-boundaries` cleans up extra word boundaries from
    TextGrids -- i.e. empty space between words.
- Configuration file for project specific settings like Tier names, if an
  utterance level should be included, and a bunch of other things.
- An update to this README, possibly with easier installation.
- Documentation.

## Installation

### New ways while waiting for upload to pypi

- Follow the instructions in the [docs](docs/Install_cast.markdown)
  (recommended), or
- You could also ask Pertti for the wheel files and install from them, or
- Do a [developer
  install](docs/Development_guide.markdown#install-cast-in-development-mode-)
  although this will not be easy, or
- Use the old way described below.

### Old way

Following steps should lead to a working installation. Please, let me know if
anything doesn't work and especially if you have a fix/update for this method. I
have only very superficially tested installation on Linux and not at all on any
other systems.

- Get Conda and Mamba.
- Either:
  - Get git and (fork and) clone the repository to your local system or
  - download the repository.
- Create the virtual environment for CAST with
  `mamba create -f cast_stable_conda_env.yaml` and activate it with
  `conda activate cast_stable`.
- If everything worked, you can run cast by calling `python cast.py [config
  file]`. See [Running](#running) below for more instructions.

## Files and directories

- [source/computer_assisted_segmentation_tools](source/computer_assisted_segmentation_tools)
  is the directory that contains the processing logic.
- `cast` or `computer-assisted-segmentation-tools` is the commandline interface
  for CAST.
- .gitignore tells git which directories and files to ignore.
- local_files/ is not included in the distribution, but it is ignored by git. If
  you are working on CAST with git, this is the place to put your local test
  files and generated results to keep git from seeing them.
- cast_exclude_example.yml is an example of an exclusion list. The file is
  commented to make it easier to create your own based on it. To avoid a host of
  issues, the format is Strict YAML rather than regular YAML. Refer to
  documentation [here](https://hitchdev.com/strictyaml/) for details of the
  format and the file itself for how fields are handled.
- cast_stable_conda_env.yaml is the specification for the conda/python virtual
  environment in which CAST runs. Probably easiest to build with mamba rather
  than conda.

## Code

CAST is written in Python with some external packages and configuration/setting
files in StrictYAML. Some of the code base (particularly ) is shared with SATKIT
and there is a possibility that CAST will become a submodule in SATKIT or that
there will be some other kind of integration to avoid code duplication.

## Running

First, create a config `.yaml` file with the correct options. There are some
examples included with CAST.

### Concatenation

To concatenate, run either `python cast.py config.yaml` or `python cast.py
concatenate config.yaml`.

DEPRECATION NOTICE: The default status of the concatenate command should already
be considered deprecated. In the future, CAST will most likely be integrated into
SATKIT and the default will be to create the individual TextGrids directly with
pre-generated (dumb) segmentation. This is because SATKIT makes it easy to edit
a lot of individual recordings without needing to do the 'select objects - open
for editing - edit - save - close window - start again with select object' dance
that Praat requires.

### Extraction

To extract run `python cast.py extract config.yaml`.

NOTE! Any existing TextGrids will currently be overwritten without warning.
