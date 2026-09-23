from pathlib import Path

from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.message.GDT_HTML import GDT_HTML
from gdo.ui.GDT_SearchTerm import GDT_SearchTerm


class search(Method):

    PREVIEW_WORDS = 4

    @classmethod
    def gdo_trigger(cls) -> str:
        return "zens"

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_SearchTerm('search_term').not_null().positional(),
        ]

    @classmethod
    def matching_scrolls(cls, scrolls_dir: str, term: str) -> list[tuple[int, str]]:
        matches = []
        paths = (path for path in Path(scrolls_dir).iterdir() if path.is_file() and path.name.isdigit())
        for path in sorted(paths, key=lambda item: int(item.name)):
            wisdom = path.read_text(encoding='utf-8')
            if term.casefold() in wisdom.casefold():
                matches.append((int(path.name), wisdom))
        return matches

    @classmethod
    def preview(cls, number: int, wisdom: str) -> str:
        words = wisdom.split()[:cls.PREVIEW_WORDS]
        return f'{number}) {" ".join(words)}'

    @classmethod
    def format_matches(cls, matches: list[tuple[int, str]]) -> str:
        if len(matches) == 1:
            number, wisdom = matches[0]
            return f'{number}) {wisdom}'
        return ' | '.join(cls.preview(number, wisdom) for number, wisdom in matches)

    async def gdo_execute(self) -> GDT:
        term = self.param_value('search_term')
        scrolls_dir = self.gdo_module().file_path(f'/anonymous-zen-book/')
        return GDT_HTML().html(self.format_matches(self.matching_scrolls(scrolls_dir, term)))
