from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.base.Util import get_module, Random
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_User import GDT_User
from gdo.slapwarz.GDO_Slap import GDO_Slap


class slap(Method):

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'slap'

    def gdo_in_private(self) -> bool:
        return False

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_User('target').same_channel(self._env_channel).online().not_null(),
        ]

    def get_target(self) -> GDO_User:
        return self.param_value('target')

    async def gdo_execute(self) -> GDT:
        target = self.get_target()
        slaps = get_module('slapwarz').load_slaps()
        adverb = Random.list_item(slaps['adverbs'])
        verb = Random.list_item(slaps['verbs'])
        adjective = Random.list_item(slaps['adjectives'])
        noun = Random.list_item(slaps['nouns'])
        if GDO_Slap.is_remainslap(self._env_user, target):
            score = -get_module('slapwarz').cfg_remainslap_malus()
        else:
            score = (adverb[1]-10) * (verb[1]-10) * (adjective[1]-10) * (noun[1]-10) // (1337 * 3)
        slap = GDO_Slap.blank({
            'slap_attacker': self._env_user.get_id(),
            'slap_defender': target.get_id(),
            'slap_points': str(score),
            'slap_adverb': str(adverb[0]),
            'slap_verb': str(verb[0]),
            'slap_adjective': str(adjective[0]),
            'slap_noun': str(noun[0]),
        }).insert()
        return self.msg('%s', (slap.render_message(),))
