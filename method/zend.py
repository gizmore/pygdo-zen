from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.core.GDT_Bool import GDT_Bool


class zend(Method):

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'zend'

    def gdo_user_type(self) -> str | None:
        return 'member,guest,link'

    def gdo_parameters(self) -> list[GDT]:
        return [GDT_Bool('enabled').not_null().positional()]

    def gdo_execute(self) -> GDT:
        enabled = self.param_value('enabled')
        self._env_user.save_setting('zend', '1' if enabled else '0')
        return self.reply('msg_zend_subscription', ('enabled' if enabled else 'disabled',))
