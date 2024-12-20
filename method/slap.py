from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDT_User import GDT_User


class slap(Method):

    def gdo_trigger(self) -> str:
        return 'slap'

    def gdo_in_private(self) -> bool:
        return False

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_User('target').same_channel(True).online().not_null(),
        ]

    async def gdo_execute(self) -> GDT:
        user = self.param_value('target')
        return self.empty()
