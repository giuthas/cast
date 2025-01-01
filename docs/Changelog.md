# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[//]: # (Possible headings in a release:)
[//]: # (Highlights for shiny new features.)
[//]: # (Added for new features.)
[//]: # (Changed for changes in existing functionality.)
[//]: # (Refactor when functionality does not change but moves.)
[//]: # (Documentation for updates to docs.)
[//]: # (Testing for updates to tests.)
[//]: # (Deprecated for soon-to-be removed features.)
[//]: # (Removed for now removed features.)
[//]: # (Fixed for any bug fixes.)
[//]: # (Security in case of vulnerabilities.)
[//]: # (New contributors for first contributions.)

[//]: # (And ofcourse if a version needs to be YANKED:)
[//]: # (## [version number] [data] [YANKED])


## [Unreleased]

### Added

- CAST will soon be available on pypi.

As mentioned in the README these are planned features:
- `add` which add Tiers to TextGrids up to the specified level (see below).
  `add` will also generate the TextGrids if they do not already exist.
  - The Tier levels will be L0=[File], L1=[Utterance], L2=Word, L3=Phonemes,
    L4=Phones. Levels whose names are in brackets can be turned off as a
    configuration option. All preceding levels (that haven't been turned off) above
    the requested level will be added to the TextGrid. The File level is turned off
    by default when not running `concatenate`. All levels maybe renamed as a
    configuration option.
- `concatenate` produces a concatenated wav file and corresponding TextGrid
  for working on multiple recordings in Praat.
- `extract` extracts TextGrids corresponding to individual recordings from a
  previously concatenated set of recordings.
- `remove-double-word-boundaries` cleans up extra word boundaries from
  TextGrids -- i.e. empty space between words.
- Configuration file for project specific settings like Tier names, if an
  utterance level should be included, and a bunch of other things.

In addition:
- Support for beep detection (go-signal in delayed naming experiments), and
  automatically adding the relevant intervals in the TextGrids.

### Changed 

- `add` currently writes the TextGrids in the original data directory. This
  maybe changed in the future or become optional, but is pending on SATKIT being
  able to properly edit TextGrids because Praat doesn't have a very easy time with
  TextGrids and wavs living in separate directories.

### Removed

- Lots of old code, so please don't rely on the API staying very stable before
  version 1.0.

## [0.2.0]

### Highlights

- `add` and `delete` work.

### Added

- `add` applies exclusion list before processing files.
- `add` moves existing textgrids to a safe directory before creating new tiers
  and writing the new textgrids in the original directory.
- `add` now does incremental adding of Tiers.
- `delete` can be used to remove Tiers incrementally.
- A number of other commands are present in the command line interface too, but
  have not been implemented yet.

### Removed

- File tier level is now by default off even if it is not explicitly set in the
  configuration.
- Similarly, Utterance, Word, Phoneme, and Phone are by default on.
- Removed read_na_list which was used to read old style exclusion text files.

## [0.1.0] 2024-10-08

### Added

- After installation CAST can now be executed as a regular command -- `cast` or
  `computer_assisted_segmentation_tools` from the commandline (no need to call
  Python or run it from a specific directory).
- `cast add` now works for utterance Tiers for TextGrids newly generated from AAA
  metadata. 

### Removed

- Old commandline script at project root.
- Support for yaml config files that had spaces in variable names.

### Known issues

- `concatenate` does not work yet, nor does `add` yet work with concatenated
  data.
