from functools import lru_cache

import tomlkit

from gdo.base.GDO_Module import GDO_Module
from gdo.slapwarz.GDO_Slaps import GDO_Slaps


class module_slapwarz(GDO_Module):

    @lru_cache
    def load_slaps(self) -> dict:
        with open(self.file_path('slaps.toml'), "r") as fh:
            return tomlkit.load(fh)

    def gdo_classes(self):
        return [
            GDO_Slaps,
        ]
