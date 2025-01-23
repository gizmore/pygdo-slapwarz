from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_String import GDT_String
from gdo.core.GDT_UInt import GDT_UInt
from gdo.core.GDT_User import GDT_User
from gdo.date.GDT_Created import GDT_Created


class GDO_Slaps(GDO):

    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_AutoInc('slap_id'),
            GDT_User('slap_attacker').not_null().cascade_delete(),
            GDT_User('slap_defender').not_null().cascade_delete(),
            GDT_UInt('slap_points').bytes(2).not_null(),
            GDT_String('slap_adverb').not_null().ascii().maxlen(32),
            GDT_String('slap_verb').not_null().ascii().maxlen(32),
            GDT_String('slap_adjective').not_null().ascii().maxlen(32),
            GDT_String('slap_item').not_null().ascii().maxlen(32),
            GDT_Created('slap_created'),
        ]
