import os

from gdo.base.Application import Application
from gdo.base.ModuleLoader import ModuleLoader
from gdo.core.method.clear_cache import clear_cache
from gdotest.TestUtil import GDOTestCase, install_module, cli_plug


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
