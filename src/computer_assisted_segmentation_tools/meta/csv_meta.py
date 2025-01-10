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
from contextlib import closing
from csv import DictReader
from pathlib import Path
import sys


def add_prompt_info(table: list[dict], csv_meta_file: Path):
    """
    Read AAA prompt file and add metadata from it to the table.

    Parameters
    ----------
    table : dict
        _description_
    csv_meta_file : Path
        _description_
    """
    meta_dict = {}
    with closing(open(csv_meta_file, 'r', encoding='utf8')) as meta_file:
        reader = DictReader(meta_file)
        for row in reader:
            meta_dict[row['id']] = row['ortho']

    for item in table:
        item['prompt'] = meta_dict[item['token_id']]


def check_and_load_csv_meta(speaker_id: str, directory: Path,
                            test: bool, csv_meta_file: Path) -> list[dict]:
    """
    Currently not supported.

    This is a concept for providing initial metadata as a csv file that will
    be used for specifying prompts/orthographic content for each sound file.

    Parameters
    ----------
    speaker_id : str
        _description_
    directory : Path
        _description_
    test : bool
        _description_
    csv_meta_file : Path
        _description_

    Returns
    -------
    list[dict]
        _description_
    """
    # Since we are concerned with audio annotation, wav files
    # determine the name list for all other files.
    wav_files = sorted(directory.glob('*.wav'))
    if len(wav_files) < 1:
        print(f"Didn't find any sound files to concatenate in {directory}.")
        sys.exit()

    # for test runs do only first ten files:
    if test and len(wav_files) >= 10:
        wav_files = wav_files[:10]

    prompt_files = sorted(directory.glob('*.txt'))
    if len(prompt_files) < 1:
        print(f"Didn't find any prompt files in {directory}.")
        sys.exit()

    # initialise table with the speaker_id and name repeated, wav_file name
    # from the list, and other fields empty
    table = [{
        'excluded': False,
        'filename': wavfile.stem,
        'wav_path': wavfile,
        'token_id': wavfile.stem[6:10].replace('_', '.'),
        'prompt_path': None,
        'ultra_path': None,
        'id':wavfile.stem,
        'speaker':speaker_id,
        'sliceBegin':'n/a',
        'begin':'n/a',
                'end':'n/a',
                'prompt':'n/a'}
             for wavfile in wav_files]

    add_prompt_info(table, csv_meta_file)

    return table
