from gdo.base.GDT import GDT
from gdo.base.GDO import GDO
from gdo.base.Trans import t
from gdo.base.Util import get_module
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_String import GDT_String
from gdo.core.GDT_User import GDT_User
from gdo.date.GDT_Created import GDT_Created
from gdo.ui.GDT_Score import GDT_Score


class GDO_Slap(GDO):

    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_AutoInc('slap_id'),
            GDT_User('slap_attacker').not_null().cascade_delete(),
            GDT_User('slap_defender').not_null().cascade_delete(),
            GDT_Score('slap_points').bytes(2).not_null(),
            GDT_String('slap_adverb').not_null().ascii().maxlen(32),
            GDT_String('slap_verb').not_null().ascii().maxlen(32),
            GDT_String('slap_adjective').not_null().ascii().maxlen(32),
            GDT_String('slap_noun').not_null().ascii().maxlen(32),
            GDT_Created('slap_created'),
        ]

    def get_attacker(self) -> GDO_User:
        return self.gdo_value('slap_attacker')

    def get_defender(self) -> GDO_User:
        return self.gdo_value('slap_defender')

    @classmethod
    def is_remainslap(cls, attacker: GDO_User, defender: GDO_User) -> bool:
        if last := cls.table().get_by_vals({'slap_attacker': attacker.get_id(), 'slap_defender': defender.get_id()}):
            return GDT_Created.column(last, 'slap_created').get_elapsed() < get_module('slapwarz').cfg_remainslap_timeout()
        return False

    def render_message(self) -> str:
        key = 'msg_slapwarz_remain_slap' if self.gdo_value('slap_points') < 0 else 'msg_slapwarz_slap'
        return t(key, (self.get_attacker().render_name(), self.gdo_val('slap_adverb'), self.gdo_val('slap_verb'), self.get_defender().render_name(), self.gdo_val('slap_adjective'), self.gdo_val('slap_noun'), self.gdo_value('slap_points')))
