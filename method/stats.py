from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDT_Bool import GDT_Bool
from gdo.core.GDT_User import GDT_User


class stats(Method):

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'slap.stats'

    def gdo_in_private(self) -> bool:
        return False

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_Bool('global').initial('0'),
            GDT_User('user'),
        ]

    def gdo_execute(self) -> GDT:
        pass
