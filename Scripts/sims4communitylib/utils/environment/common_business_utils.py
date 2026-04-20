"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) DEVIANTGAMEMODS
"""
from typing import Union

from business.business_funds import BusinessFunds
from business.business_manager import BusinessManager
from business.business_service import BusinessService
from sims.sim_info import SimInfo


class CommonBusinessUtils:
    """Utilities for manipulating Businesses."""

    @classmethod
    def is_customer_of_business(cls, sim_info: SimInfo, business_manager: BusinessManager) -> bool:
        """is_customer_of_business(sim_info, business_manager)

        Determine if a Sim is a customer of the specified business.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param business_manager: The business manager to check.
        :type business_manager: BusinessManager
        :return: True, if the Sim is a customer of the specified Business. False, if not.
        :rtype: bool
        """
        if not hasattr(business_manager, '_customer_manager') or business_manager._customer_manager is None:
            return False
        return business_manager._customer_manager.is_sim_a_customer(sim_info)

    @classmethod
    def is_employee_of_business(cls, sim_info: SimInfo, business_manager: BusinessManager) -> bool:
        """is_employee_of_business(sim_info, business_manager)

        Determine if a Sim is an employee of the specified business.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :param business_manager: The business manager to check.
        :type business_manager: BusinessManager
        :return: True, if the Sim is an employee of the specified Business. False, if not.
        :rtype: bool
        """
        return business_manager.is_employee(sim_info)

    @classmethod
    def get_business_manager_for_current_zone(cls) -> BusinessManager:
        """get_business_manager_for_current_zone()

        Retrieve a Business Manager for the current Zone.

        :return: A Business Manager for the current zone.
        :rtype: BusinessManager
        """
        from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
        return cls.get_business_manager_by_zone_id(CommonLocationUtils.get_current_zone_id())

    @classmethod
    def get_business_manager_by_zone_id(cls, zone_id: int) -> BusinessManager:
        """get_business_manager_by_zone_id(zone_id)

        Retrieve a Business Manager for a Zone.

        :param zone_id: The identifier of the Zone to retrieve a Business Manager from.
        :type zone_id: int
        :return: A Business Manager for the specified zone.
        :rtype: BusinessManager
        """
        return cls.get_business_service().get_business_manager_for_zone(zone_id=zone_id)

    @classmethod
    def get_business_funds_for_current_zone(cls) -> Union[BusinessFunds, None]:
        """get_business_funds_for_current_zone()

        Retrieve the Funds object that manages the Simoleons for the Business of the current Zone.

        :return: The BusinessFunds object of the Business at the current Zone or None if the current Zone did not have a Business.
        :rtype: Union[BusinessFunds, None]
        """
        from sims4communitylib.utils.location.common_location_utils import CommonLocationUtils
        return cls.get_business_funds_by_zone_id(CommonLocationUtils.get_current_zone_id())

    @classmethod
    def get_business_funds_by_zone_id(cls, zone_id: int) -> Union[BusinessFunds, None]:
        """get_business_funds_by_zone_id(zone_id)

        Retrieve the Funds object that manages the Simoleons for the Business of a Zone.

        :param zone_id: The identifier of the Zone to retrieve a Business from. Default is the current zone.
        :type zone_id: int, optional
        :return: The BusinessFunds object of the Business at the specified zone or None if the specified Zone did not have a Business.
        :rtype: Union[BusinessFunds, None]
        """
        business_manager = CommonBusinessUtils.get_business_manager_by_zone_id(zone_id)
        if business_manager is None:
            return
        return business_manager.funds

    @classmethod
    def get_business_service(cls) -> BusinessService:
        """get_business_service()

        Retrieve an instance of the Business Service.

        :return: An instance of the Business Service.
        :rtype: BusinessService
        """
        import services
        return services.business_service()
