"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) DEVIANTGAMEMODS
"""
from typing import Union

import services
from family_tree.family_tree_service import FamilyTreeService
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimFamilyTreeUtils:
    """Utilities for managing and manipulating the Family Tree of Sims."""
    @classmethod
    def get_family_tree_service(cls) -> Union[FamilyTreeService, None]:
        """get_family_tree_service()

        Retrieve the Family Tree Service.

        :return: The family tree service or None if not found.
        :rtype: Union[FamilyTreeService, None]
        """
        return services.family_tree_service()

    @classmethod
    def are_blood_related(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """are_blood_related(sim_info_a, sim_info_b)

        Determine if Sim A is blood related to Sim B.

        :return: True, if Sim A is blood related to Sim B. False, if not.
        :rtype: bool
        """
        if sim_info_a is None or sim_info_b is None:
            return False
        family_tree_service = cls.get_family_tree_service()
        sim_id_a = CommonSimUtils.get_sim_id(sim_info_a)
        sim_id_b = CommonSimUtils.get_sim_id(sim_info_b)
        return family_tree_service.are_sims_blood_related(sim_id_a, sim_id_b)
