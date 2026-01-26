from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.base.Util import Files, Random
from gdo.core.GDT_UInt import GDT_UInt
from gdo.message.GDT_HTML import GDT_HTML


class zen(Method):

    @classmethod
    def gdo_trigger(cls) -> str:
        return "zen"

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_UInt('number').min(1).max(159).not_null(False).positional(),
        ]

    def gdo_execute(self) -> GDT:
        num = self.param_value('number') or Random.mrand(1, 159) # RNG chosen by Alice.
        wisdom = str(num) + ") " + Files.get_contents(self.gdo_module().file_path(f'/anonymous-zen-book/{num}'))
        return GDT_HTML().html(wisdom)
