from functools import lru_cache

import tomlkit

from gdo.base.GDO_Module import GDO_Module
from gdo.base.GDT import GDT
from gdo.date.GDT_Duration import GDT_Duration
from gdo.slapwarz.GDO_Slap import GDO_Slap
from gdo.ui.GDT_Score import GDT_Score
from gdo.base.GDO import GDO


class module_slapwarz(GDO_Module):

    @lru_cache
    def load_slaps(self) -> dict:
        with open(self.file_path('slaps.toml'), "r") as fh:
            return tomlkit.load(fh)

    def gdo_classes(self) -> list[type[GDO]]:
        return [
            GDO_Slap,
        ]

    def gdo_module_config(self) -> list[GDT]:
        return [
            GDT_Duration('slap_timeout').initial('1d').not_null(),
            GDT_Score('slap_remain_score').initial('50').not_null().min(0),
        ]

    def cfg_remainslap_malus(self) -> int:
        return self.get_config_value('slap_remain_score')

    def cfg_remainslap_timeout(self) -> float:
        return self.get_config_value('slap_timeout')
