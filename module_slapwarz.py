import tomlkit

from gdo.base.GDO_Module import GDO_Module


class module_slapwarz(GDO_Module):

    def load_slaps(self) -> dict:
        path = self.file_path('slaps.toml')
        with open(path, "r") as fh:
            return tomlkit.load(fh)