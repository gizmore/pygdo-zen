import subprocess

from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.message.GDT_HTML import GDT_HTML
from gdo.ui.GDT_SearchTerm import GDT_SearchTerm


class search(Method):

    @classmethod
    def gdo_trigger(cls) -> str:
        return "zens"

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_SearchTerm('search_term').not_null().positional(),
        ]

    async def gdo_execute(self) -> GDT:
        term = self.param_value('search_term')
        scrolls_dir = self.gdo_module().file_path(f'/anonymous-zen-book/')
        res = subprocess.run(
            ['bash', 'search.sh', term],
            cwd=scrolls_dir,
            capture_output=True,
            text=True,
        )
        return GDT_HTML().html(res.stdout)
