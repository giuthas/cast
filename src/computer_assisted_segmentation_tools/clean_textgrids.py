#
# Copyright (c) 2022-2024 Pertti Palo.
#
# This file is part of Computer Assisted Segmentation Tools 
# (see https://github.com/giuthas-speech-research-tools/cast/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# The example data packaged with this program is licensed under the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International (CC BY-NC-SA 4.0) License. You should have received a
# copy of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International (CC BY-NC-SA 4.0) License along with the data. If not,
# see <https://creativecommons.org/licenses/by-nc-sa/4.0/> for details.
#
# When using the toolkit for scientific publications, please cite the
# articles listed in README.markdown. They can also be found in
# citations.bib in BibTeX format.
#
import pprint
from pathlib import Path

from textgrids import TextGrid, Tier

pp = pprint.PrettyPrinter(indent=4)

def delete_interval(
    tier: Tier,
    index: int
    ):
    """
    Delete an Interval from a TextGrid Tier.

    The label of the Interval is discarded and the end time (xmax) of the
    previous Interval is set to the end time of the Interval to be deleted.

    Parameters
    ----------
    tier : Tier
        The Tier containing the Inteval to be deleted.
    index : int
        Index of the Interval to be deleted.
    """
    tier[index-1].xmax = tier[index].xmax
    del tier[index]

def remove_empty_intervals_from_grid(
        original_gridfile: Path,
        output_dir: Path
    ):
    """
    Delete all empty Intervals (excpet first and last) in every Tier.

    Any empty segments apart from the first and last Interval of each Tier get
    deleted by extending the previous Interval to cover the deleted Interval's
    time span.

    The resulting new TextGrid is written with using the original name into the
    output directory.

    Parameters
    ----------
    original_gridfile : Path
        Path to the TextGrid file.
    output_dir : Path
        Path to the output directory.
    """
    if not original_gridfile.exists():
        print("Error: Original TextGrid file - " + str(original_gridfile) + " - does not exist.")

    if not output_dir.exists():
        output_dir.mkdir()

    grid = TextGrid(original_gridfile)
    for tier in grid:
        deletion_list =  []
        for i, interval in enumerate(grid[tier][1:-1]):
            if not interval.text:
                deletion_list.append(i+1)
        deletion_list.reverse()
        for i in deletion_list:
            delete_interval(grid[tier], i)
    output_path = output_dir/original_gridfile.name
    grid.write(output_path)


# TODO: change this into a generic filtering function which takes a list of
# filters to apply to each texgrid. 
def remove_empty_intervals_from_textgrids(
        original_dir: Path, 
        output_dir: Path,
    ):
    """
    Remove empty intervals from all TextGrids in the given directory.

    Parameters
    ----------
    original_dir : Path
        Path to directory which contains the original TextGrids.
    output_dir : Path
        Path to the output directory.
    """
    if not original_dir.exists():
        print("Fatal: Directory of original TextGrids does not exist.")
        exit()

    if not output_dir.exists():
        output_dir.mkdir()

    for textgrid in original_dir.glob("*.TextGrid"):
        remove_empty_intervals_from_grid(textgrid, output_dir)
