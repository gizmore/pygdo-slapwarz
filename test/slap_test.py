import os

from gdo.base.Application import Application
from gdo.base.ModuleLoader import ModuleLoader
from gdo.core.connector.Bash import Bash
from gdo.core.GDO_Channel import GDO_Channel
from gdo.core.GDT_User import GDT_User
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
        server = Bash.get_server()
        peter = await server.get_or_create_user('Peter')
        channel = server.get_or_create_channel('test_channel')
        await channel.on_user_joined(peter)
        gizmore = cli_gizmore()
        out = cli_plug(gizmore, '$slap peter')
        self.assertIn('gizmore', out, 'gizmore not in message')

    async def test_02_channel_user_completion_uses_user_names(self):
        server = Bash.get_server()
        peter = await server.get_or_create_user('Peter')
        channel = GDO_Channel.blank({
            'chan_server': server.get_id(),
            'chan_name': '#slap-test',
            'chan_displayname': '#slap-test',
            'chan_language': 'en',
            'chan_trigger': '$',
        }).insert()
        await channel.on_user_joined(peter)

        target = GDT_User('target').same_channel(channel)
        target.val('peter')
        self.assertEqual(peter.get_id(), target.get_value().get_id())
        self.assertTrue(channel.is_user_online(peter))
