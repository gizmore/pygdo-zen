import os
from unittest.mock import Mock

from gdo.base.Application import Application
from gdo.base.ModuleLoader import ModuleLoader
from gdo.base.Render import Mode
from gdo.core.method.clear_cache import clear_cache
from gdotest.TestUtil import GDOTestCase, install_module, cli_plug
from gdo.zen.method.zend import zend
from gdo.zen.method.search import search
from gdo.zen.module_zen import module_zen


class ZenTest(GDOTestCase):

    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()
        Application.init(os.path.dirname(__file__ + "/../../../../"))
        loader = ModuleLoader.instance()
        loader.load_modules_db(True)
        install_module('zen')
        Application.init_cli()
        loader.init_modules(True, True)
        loader.init_cli()
        await clear_cache().gdo_execute()

    async def test_01_zen(self):
        out = cli_plug(None, '$zen 1')
        self.assertIn('world', out, 'zen did not work nicely on all continents.')

    async def test_02_zend_subscription(self):
        method = object.__new__(zend)
        method._env_user = Mock()
        method.param_value = Mock(return_value=True)
        method.reply = Mock()

        method.gdo_execute()

        method._env_user.save_setting.assert_called_once_with('zend', '1')
        method.reply.assert_called_once_with('msg_zend_subscription', ('enabled',))

    def test_03_search_multiple_preview(self):
        matches = [
            (81, 'There is no wisdom, if you judge too early.'),
            (144, 'You should not trust me blindly.'),
        ]
        self.assertEqual(
            '81) There is no wisdom, | 144) You should not trust',
            search.format_matches(matches),
        )

    def test_04_search_single_full_scroll(self):
        self.assertEqual('1) A complete scroll.\n', search.format_matches([(1, 'A complete scroll.\n')]))

    def test_05_irc_wisdom_is_one_line(self):
        wisdom = 'One line.\nAnother line.\n\nThe end.\n'
        self.assertEqual('One line. Another line. The end.', module_zen.format_wisdom(wisdom, Mode.render_irc))
        self.assertEqual(wisdom, module_zen.format_wisdom(wisdom, Mode.render_cli))
