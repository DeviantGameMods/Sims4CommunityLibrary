"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) DEVIANTGAMEMODS
"""
from typing import Union

from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog
from situations.service_npcs.service_npc_manager import ServiceNpcService
from zone import Zone


class CommonServiceNPCUtils(_HasS4CLClassLog):
    """Utilities for NPC Services.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_sim_npc_service_utils'

    @classmethod
    def get_service_npc_service_for_current_zone(cls) -> ServiceNpcService:
        """get_service_npc_service_for_current_zone()

        Retrieve the Service for Service NPCs tied to the current Zone.

        :return: The service for Service NPCs tied to the current zone.
        :rtype: ServiceNpcService
        """
        from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
        # noinspection PyUnresolvedReferences
        return CommonLocationUtils.get_current_zone().service_npc_service

    @classmethod
    def get_service_npc_service(cls, zone: Union[int, Zone]) -> Union[ServiceNpcService, None]:
        """get_service_npc_service(zone)

        Retrieve the Service for Service NPCs tied to a Zone.

        :param zone: The zone the service is tied to.
        :type zone: Zone
        :return: The service for Service NPCs tied to the specified zone or None if no service is found.
        :rtype: Union[ServiceNpcService, None]
        """
        from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
        zone_instance = CommonLocationUtils.get_zone(zone)
        if zone_instance is None:
            return None
        # noinspection PyUnresolvedReferences
        return zone_instance.service_npc_service
