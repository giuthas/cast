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
"""Console script for computer_assisted_segmentation_tools."""

import click

from . import cast_click
# from .command_line import CastArgumentParser
# from .commands import CommandStrings, process_command
# from .configuration import CastConfig
# from .exclusion import load_exclusion_list


@click.group()
@click.version_option()
@click.pass_context
def run_cli(context: click.Context) -> None:
    """
    CAST - Computer Assisted Segmentation Tools

    Cast is mainly used to add new Tiers to TextGrids. See documentation for
    details.
    """
    pass

    # cli = CastArgumentParser("CAST")
    #
    # command_string = cli.args.command
    # if command_string in CommandStrings.values():
    #     command = CommandStrings(command_string)
    #     path = cli.args.path
    #     if cli.args.config_file:
    #         config_file = Path(cli.args.config_file)
    #     else:
    #         config_file = path / "cast_config.yaml"
    #     config = CastConfig(config_file.main_config)
    #
    #     if config.exclusion_list:
    #         exclusion_file = config.exclusion_list
    #     else:
    #         exclusion_file = Path(cli.args.exclusion_filename)
    #         config.exclusion_list = exclusion_file
    #     exclusion_list = load_exclusion_list(exclusion_file)
    #
    #     process_command(command=command,
    #                     path=path,
    #                     config=config,
    #                     exclusion_list=exclusion_list)
    # else:
    #     print("Did not find a command in the arguments: " +
    #           cli.args.command + ".")
    #     print(f"Accepted commands are: {', '.join(CommandStrings.values())}")


# noinspection PyTypeChecker
run_cli.add_command(cast_click.add)
# noinspection PyTypeChecker
run_cli.add_command(cast_click.concatenate)
# noinspection PyTypeChecker
run_cli.add_command(cast_click.extract)
# noinspection PyTypeChecker
run_cli.add_command(cast_click.delete)
# noinspection PyTypeChecker
run_cli.add_command(cast_click.init)
# noinspection PyTypeChecker
run_cli.add_command(cast_click.remove_double_boundaries)
# noinspection PyTypeChecker
run_cli.add_command(cast_click.scramble)
