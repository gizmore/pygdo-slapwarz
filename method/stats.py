from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.base.Trans import t
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_Enum import GDT_Enum
from gdo.core.GDT_UInt import GDT_UInt
from gdo.core.GDT_User import GDT_User
from gdo.date.Time import Time
from gdo.slapwarz.GDO_Slap import GDO_Slap


class stats(Method):

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'slaps'

    def gdo_in_private(self) -> bool:
        return False

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_UInt('page').initial('1').max(GDO_Slap.table().count_where()),
            GDT_Enum('type').choices({'dealt': 'dealt', 'taken': 'taken', 'score': 'score', 'hits': 'hits', 'damage': 'damage'}).initial('hits').not_null().positional(),
            GDT_User('user').positional().myself(),
        ]

    def get_target(self) -> GDO_User:
        return self.param_value('user')

    def gdo_execute(self) -> GDT:
        type = self.param_val('type')
        target = self.get_target()
        query = GDO_Slap.table().query()
        query.select(GDO.quote(target.render_name())) if target else query.select(GDO.quote(t('overall')))
        key = ''
        if type == 'dealt':
            query.select('SUM(slap_points), COUNT(*)')
            key = "msg_slap_stats_dealt"
            if target:
                query.where(f'slap_attacker={target.get_id()}')

        if type == 'taken':
            query.select('SUM(slap_points), COUNT(*)')
            key = "msg_slap_stats_taken"
            if target:
                query.where(f'slap_defender={target.get_id()}')

        if type == 'score':
            query.select('SUM(slap_points), COUNT(*)')
            key = "msg_slap_stats_score"
            if target:
                query.where(f'slap_attacker={target.get_id()} OR slap_defender={target.get_id()}')

        if type == 'hits':
            where = f'slap_attacker={target.get_id()}' if target else '1'
            query.select(f'(SELECT COUNT(*) FROM gdo_slap WHERE {where} AND slap_points >= 0)')
            query.select(f'(SELECT SUM(slap_points) FROM gdo_slap WHERE {where} AND slap_points >= 0)')
            query.select(f'(SELECT COUNT(*) FROM gdo_slap WHERE {where} AND slap_points < 0)')
            query.select(f'(SELECT SUM(slap_points) FROM gdo_slap WHERE {where} AND slap_points < 0)')
            query.select(f'(SELECT COUNT(*) FROM gdo_slap WHERE {where})')
            query.select(f'(SELECT SUM(slap_points) FROM gdo_slap WHERE {where})')
            key = "msg_slap_stats_hits"

        if type == 'damage':
            top_slap = GDO_Slap.table().select().order('slap_points DESC').limit(1, self.param_value('page')-1).exec().fetch_object()
            query.select(GDO.quote(top_slap.gdo_val('slap_points')))
            query.select(GDO.quote(top_slap.render_message()))
            query.select(GDO.quote(Time.display_date(top_slap.gdo_val('slap_created'))))
            query.select(GDO.quote(Time.display_age(top_slap.gdo_val('slap_created'))))
            key = "msg_slap_stats_damage"
            if target:
                query.where(f'slap_attacker={target.get_id()}')

        result = tuple(query.exec().fetch_row())
        return self.msg(key, result)
