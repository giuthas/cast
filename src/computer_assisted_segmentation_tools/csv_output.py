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

import csv
from contextlib import closing


def write_fav_input(table, filename):
    """
    Write the metadata into a csv-formated file to be read by FAVE.
    """
    # extrasaction='ignore' does not seem to be working so we do this the long way
    fieldnames = ['id', 'speaker', 'begin', 'end', 'word']
    results = [{key: entry[key] for key in fieldnames} for entry in table]

    with closing(open(filename, 'w', encoding='utf8')) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                delimiter='\t', quoting=csv.QUOTE_NONE)

        list(map(writer.writerow, results))
    print("Wrote file " + filename + " for FAVE align.")


def write_results(table, filename, detect_beep):
    """ 
    Write the metadata into a csv-formated file to be read by Python or R.

    This file is meant for the extraction script but also possibly
    used by later analysis stages.
    """
    # extrasaction='ignore' does not seem to be working so we do this the long way
    if detect_beep:
        fieldnames = ['id', 'speaker', 'sliceBegin',
                      'beep', 'begin', 'sliceEnd', 'prompt']
    else:
        fieldnames = ['id', 'speaker', 'sliceBegin',
                      'begin', 'sliceEnd', 'prompt']
    results = [{key: entry[key] for key in fieldnames} for entry in table]

    with closing(open(filename, 'w', encoding='utf8')) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                quoting=csv.QUOTE_NONNUMERIC)

        writer.writeheader()
        list(map(writer.writerow, results))
    print(f"Wrote file {filename} for R/Python.")
