import os

from gdo.base.Application import Application
from gdo.base.ModuleLoader import ModuleLoader
from gdo.core.connector.Bash import Bash
from gdotest.TestUtil import GDOTestCase, install_module, reinstall_module, cli_gizmore, cli_plug


class slap_test(GDOTestCase):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        Application.init(os.path.dirname(__file__ + "/../../../../"))
        loader = ModuleLoader.instance()
        loader.load_modules_db(True)
        loader.init_modules(True, True)
        install_module('pm')
        loader.init_cli()

    async def test_00_install(self):
        reinstall_module('pm')
        self.assertEqual(1, 1, 'oops')

    async def test_01_slap(self):
        peter = await Bash.get_server().get_or_create_user('Peter')
        gizmore = cli_gizmore()
        out = cli_plug(gizmore, '$slap peter')
        self.assertIn('gizmore', out, 'gizmore not in message')
