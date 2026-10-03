import random
from datetime import datetime
from zoneinfo import ZoneInfo

from gdo.base.Application import Application
from gdo.base.GDO_Module import GDO_Module
from gdo.base.GDT import GDT
from gdo.base.Logger import Logger
from gdo.base.Render import Mode
from gdo.base.Util import Files
from gdo.core.GDO_UserSetting import GDO_UserSetting
from gdo.core.GDT_Bool import GDT_Bool
from gdo.core.GDT_String import GDT_String


class module_zen(GDO_Module):

    ZEND_TIMEZONE = ZoneInfo('Europe/Berlin')

    def gdo_module_config(self) -> list[GDT]:
        return [
            GDT_String('zend_last_date').maxlen(10).initial(''),
        ]

    def gdo_user_settings(self) -> list[GDT]:
        return [
            GDT_Bool('zend').not_null().initial('0'),
        ]

    @staticmethod
    def format_wisdom(wisdom: str, mode: Mode) -> str:
        """IRC has no multiline message affordance; keep a scroll intact there."""
        return ' '.join(wisdom.split()) if mode == Mode.render_irc else wisdom

    def gdo_subscribe_events(self):
        Application.EVENTS.add_timer_async(20, self.zend_timer, Application.EVENTS.FOREVER)

    async def zend_timer(self):
        now = datetime.now(self.ZEND_TIMEZONE)
        today = now.date().isoformat()
        if (now.hour, now.minute) < (16, 20) or self.get_config_val('zend_last_date') == today:
            return

        # Claim the date before delivery so overlapping timer ticks cannot
        # send a second daily message.
        await self.save_config_val('zend_last_date', today)
        number = random.randint(1, 209)
        wisdom = Files.get_contents(self.file_path(f'anonymous-zen-book/{number}')).strip()
        users = (GDO_UserSetting.get_users_with_settings_query(None, [('zend', '=', '1')]).
                 exec().fetch_all())
        for user in users:
            try:
                await user.send('msg_zend_daily', (
                    number,
                    self.format_wisdom(wisdom, user.get_server().get_render_mode()),
                ))
            except Exception as ex:
                Logger.exception(ex)
