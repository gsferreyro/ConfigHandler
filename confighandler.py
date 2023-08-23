# Config Handler copyright 2023-2023 by Gustavo S. Ferreyro. All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Gustavo S. Ferreyro
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.
# GUSTAVO S. FERREYRO DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# GUSTAVO S. FERREYRO BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
# ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
Copyright (C) 2023-2023 Gustavo S. Ferreyro. All Rights Reserved.

To use, copy this module and 'import confighandler' or 'from confighandler import ConfigHandler'

This Config Handler uses the configparser package for Python.
https://github.com/python/cpython/blob/main/Lib/configparser.py
"""

import os
import errno
import configparser


class ConfigHandler(configparser.ConfigParser):
    def __init__(self, folderpath: str, name: str):
        super().__init__(os.environ)
        folderpath = os.path.normpath(folderpath)
        self.folderpath = folderpath
        if not name.lower().endswith(".ini"):
            name += ".ini"
        self.name = name
        self.filepath = os.path.normpath(os.path.join(folderpath, name))
        self._load_config()

    def _load_config(self):
        if not os.path.exists(self.filepath):
            self._init_config()
        self.read(self.filepath)

    def _init_config(self):
        if not os.path.exists(self.filepath):
            self._create_config()
        config = configparser.RawConfigParser()
        config.read(self.filepath)

        if config.has_option("DEFAULT", "OPTION"):
            config.set("DEFAULT", "OPTION", "")

        with open(self.filepath, "w") as configfile:
            config.write(configfile)

    def _create_config(self):
        config = configparser.RawConfigParser()
        config_dict = {
            "DEFAULT": {"OPTION": ""},
        }
        config.read_dict(config_dict)

        try:
            os.makedirs(self.folderpath)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            pass

        with open(self.filepath, "w") as configfile:
            config.write(configfile)

    def get(
        self,
        section,
        option,
        *,
        raw=False,
        exit_if_not_exist: bool = True,
    ):
        try:
            return super().get(section=section, option=option, raw=raw)
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            print(f"Error: {e}")
            if exit_if_not_exist:
                exit(1)
            return ""

    def getdict(
        self, section, option, dict_separator: str = ",", exit_if_not_exist: bool = True
    ):
        value = self.get(
            section=section, option=option, exit_if_not_exist=exit_if_not_exist
        ).replace(" ", "")
        dict = value.split(dict_separator) if value else []
        return dict
