from datetime import datetime

import keypirinha as kp
import keypirinha_util as kpu
from .epoch_parser import EpochParser


class Epoch(kp.Plugin):
    """
    Epoch/Unix timestamp converter

    This block is a longer and more detailed description of your plugin that may
    span on several lines, albeit not being required by the application.

    You may have several plugins defined in this module. It can be useful to
    logically separate the features of your package. All your plugin classes
    will be instantiated by Keypirinha as long as they are derived directly or
    indirectly from :py:class:`keypirinha.Plugin` (aliased ``kp.Plugin`` here).

    In case you want to have a base class for your plugins, you must prefix its
    name with an underscore (``_``) to indicate Keypirinha it is not meant to be
    instantiated directly.

    In rare cases, you may need an even more powerful way of telling Keypirinha
    what classes to instantiate: the ``__keypirinha_plugins__`` global variable
    may be declared in this module. It can be either an iterable of class
    objects derived from :py:class:`keypirinha.Plugin`; or, even more dynamic,
    it can be a callable that returns an iterable of class objects. Check out
    the ``StressTest`` example from the SDK for an example.

    Up to 100 plugins are supported per module.

    More detailed documentation at: http://keypirinha.com/api/plugin.html
    """

    ITEMCAT = kp.ItemCategory.USER_BASE + 1

    def __init__(self):
        super().__init__()

    def on_start(self):
        pass

    def on_catalog(self):
        self.set_catalog([
            self.create_item(
                category=kp.ItemCategory.KEYWORD,
                label="Epoch",
                short_desc="Epoch/Unix timestamp converter",
                target="Epoch",
                args_hint=kp.ItemArgsHint.REQUIRED,
                hit_hint=kp.ItemHitHint.IGNORE
            )
        ])

    def on_suggest(self, user_input, items_chain):
        if not items_chain or items_chain[0].category() != kp.ItemCategory.KEYWORD:
            return

        date = None
        if user_input:
            date = EpochParser.parse(user_input)
            with_epoch = False

        if date is None:
            date = datetime.now()
            with_epoch = True

        suggestions = self.__compose_suggestions(date, with_epoch)
        self.set_suggestions(suggestions, kp.Match.ANY, kp.Sort.NONE)

    def on_execute(self, item, action):
        kpu.set_clipboard(item.target())

    def on_activated(self):
        pass

    def on_deactivated(self):
        pass

    def on_events(self, flags):
        pass

    def __compose_suggestions(self, date: datetime, with_epoch: bool) -> []:
        suggestions = []

        if with_epoch:
            value = str(int(date.timestamp()))
            suggestions.append(self.__create_suggestion_item('Epoch', value, value))
            value = str(int(date.timestamp() * 1000))
            suggestions.append(self.__create_suggestion_item('Epoch with Millis', value, value))

        value = date.replace(microsecond=0).isoformat()
        suggestions.append(self.__create_suggestion_item('ISO Format', value, value))

        value = date.strftime('%d.%m.%Y %H:%M:%S')
        suggestions.append(self.__create_suggestion_item('Little Endian', value, value))

        value = date.strftime('%m/%d/%Y %H:%M:%S')
        suggestions.append(self.__create_suggestion_item('Middle Endian', value, value))

        value = date.strftime('%Y-%m-%d %H:%M:%S')
        suggestions.append(self.__create_suggestion_item('Big Endian', value, value))

        return suggestions

    def __create_suggestion_item(self, label: str, short_desc: str, target: str):
        return self.create_item(
            category=self.ITEMCAT,
            label=label,
            short_desc=short_desc,
            target=target,
            args_hint=kp.ItemArgsHint.FORBIDDEN,
            hit_hint=kp.ItemHitHint.IGNORE,
        )
