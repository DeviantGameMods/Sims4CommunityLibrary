"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) DEVIANTGAMEMODS
"""
from sims.sim_info import SimInfo
from sims4communitylib.events.event_handling.common_event import CommonEvent


class S4CLSimPregnancyEndedEvent(CommonEvent):
    """S4CLSimPregnancyEndedEvent(sim_info)

    An event that occurs after a pregnancy has ended for a Sim.

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
        from sims4communitylib.modinfo import ModInfo

        class ExampleEventListener:

            # In order to listen to an event, your function must match these criteria:
            # - The function is static (staticmethod).
            # - The first and only required argument has the name "event_data".
            # - The first and only required argument has the Type Hint for the event you are listening for.
            # - The argument passed to "handle_events" is the name of your Mod.
            @staticmethod
            @CommonEventRegistry.handle_events(ModInfo.get_identity())
            def handle_event(event_data: S4CLSimPregnancyEndedEvent):
                pass

    :param sim_info: The info of a Sim that had a pregnancy ended.
    :type sim_info: SimInfo
    """

    def __init__(self, sim_info: SimInfo):
        self._sim_info = sim_info

    @property
    def sim_info(self) -> SimInfo:
        """The info of the Sim that had a pregnancy ended.

        :return: The info of the Sim that had a pregnancy ended.
        :rtype: SimInfo
        """
        return self._sim_info
