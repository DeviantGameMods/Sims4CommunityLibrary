"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) DEVIANTGAMEMODS
"""
from typing import Union, Iterator

from family_tree.family_tree_enums import FamilyRelationBitFlags
from relationships.global_relationship_tuning import RelationshipGlobalTuning, TropeGlobalTuning
from relationships.relationship_enums import RelationshipType
from sims.genealogy_tracker import GenealogyTracker, FamilyRelationshipIndex
from sims.sim_info import SimInfo
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils


class CommonSimGenealogyUtils:
    """Utilities for managing and manipulating the Genealogy of Sims."""
    @classmethod
    def get_genealogy_tracker(cls, sim_info: SimInfo) -> Union[GenealogyTracker, None]:
        """get_genealogy_tracker(sim_info)

        Retrieve the Genealogy Tracker for a Sim.

        .. note: A Genealogy Tracker is essentially just the Family Tree Tracker of the Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The genealogy tracker of the Sim or None if not found.
        :rtype: Union[GenealogyTracker, None]
        """
        if sim_info is None:
            return None
        return sim_info._genealogy_tracker

    @classmethod
    def set_as_spouse_of(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """set_as_spouse_of(sim_info_a, sim_info_b)

        Set Sim A as the spouse of Sim B and vice verse

        :param sim_info_a: The info of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: The new spouse of Sim A.
        :type sim_info_b: SimInfo
        :return: True, if the relation was set successfully. False, if not.
        :rtype: bool
        """
        if sim_info_b.spouse_sim_id is not None:
            sim_info_a.update_spouse_sim_id(None)
        sim_id_b = CommonSimUtils.get_sim_id(sim_info_b)
        sim_info_a.update_spouse_sim_id(sim_id_b)
        return True

    @classmethod
    def set_as_fiance_of(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """set_as_fiance_of(sim_info_a, sim_info_b)

        Set Sim A as the fiance of Sim B and vice verse

        :param sim_info_a: The info of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: The new fiance of Sim A.
        :type sim_info_b: SimInfo
        :return: True, if the relation was set successfully. False, if not.
        :rtype: bool
        """
        if sim_info_b.spouse_sim_id is not None:
            sim_info_a.update_fiance_sim_id(None)
        sim_id_b = CommonSimUtils.get_sim_id(sim_info_b)
        sim_info_a.update_fiance_sim_id(sim_id_b)
        return True

    @classmethod
    def set_as_exclusive_steady_of(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """set_as_exclusive_steady_of(sim_info_a, sim_info_b)

        Set Sim A as being in an exclusive steady relationship with Sim B

        Note: All other steady relationships will be removed if they exist already!

        :param sim_info_a: The info of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: The new steady relationship of Sim A.
        :type sim_info_b: SimInfo
        :return: True, if the relation was set successfully. False, if not.
        :rtype: bool
        """
        sim_id_b = CommonSimUtils.get_sim_id(sim_info_b)
        if sim_id_b in sim_info_a._relationship_tracker.steady_sim_ids:
            return True
        steady_sim_ids = tuple(sim_info_a._relationship_tracker.steady_sim_ids)
        if steady_sim_ids:
            for sim_id in steady_sim_ids:
                sim_info_a.update_steady_sim_ids(sim_id, False)
        sim_info_a.update_steady_sim_ids(sim_id_b, True)
        return True

    @classmethod
    def set_as_father_of(cls, sim_info: SimInfo, new_child_sim_info: SimInfo, propagate: bool = False) -> bool:
        """set_as_father_of(sim_info, new_child_sim_info, propagate=False)

        Set a Sim to be the Father of another Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param new_child_sim_info: The new child of Sim A.
        :type new_child_sim_info: SimInfo
        :param propagate: Obsolete, no longer used. The family tree will ALWAYS be updated.
        :type propagate: bool, optional
        :return: True, if the relation was set successfully. False, if not.
        :rtype: bool
        """
        new_child_sim_info.set_parent_relation(FamilyRelationshipIndex.FATHER, sim_info, is_adopted=False)
        new_child_sim_info.add_family_link(sim_info)
        sim_info.add_family_link(new_child_sim_info)
        return True

    @classmethod
    def set_as_mother_of(cls, sim_info: SimInfo, new_child_sim_info: SimInfo, propagate: bool = False) -> bool:
        """set_as_mother_of(sim_info, new_child_sim_info, propagate=False)

        Set a Sim to be the Mother of another Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param new_child_sim_info: The new child of Sim A.
        :type new_child_sim_info: SimInfo
        :param propagate: Obsolete, no longer used. The family tree will ALWAYS be updated.
        :type propagate: bool, optional
        :return: True, if the relation was set successfully. False, if not.
        :rtype: bool
        """
        new_child_sim_info.set_parent_relation(FamilyRelationshipIndex.MOTHER, sim_info, is_adopted=False)
        new_child_sim_info.add_family_link(sim_info)
        sim_info.add_family_link(new_child_sim_info)
        return True

    @classmethod
    def set_as_fathers_father_of(cls, sim_info: SimInfo, new_grandchild_sim_info: SimInfo) -> bool:
        """set_as_fathers_father_of(sim_info, new_fathers_father_sim_info)

        Set a Sim to be the Fathers Father of another Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param new_grandchild_sim_info: The new grandchild of Sim A.
        :type new_grandchild_sim_info: SimInfo
        :return: True, if the relation was set successfully. False, if not.
        :rtype: bool
        """
        father_sim_info = cls.get_father_sim_info(new_grandchild_sim_info)
        cls.set_as_father_of(sim_info, father_sim_info)
        return True

    @classmethod
    def set_as_fathers_mother_of(cls, sim_info: SimInfo, new_grandchild_sim_info: SimInfo) -> bool:
        """set_as_fathers_mother_of(sim_info, new_grandchild_sim_info)

        Retrieve the Father of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param new_grandchild_sim_info: The new grandchild of Sim A.
        :type new_grandchild_sim_info: SimInfo
        :return: True, if the relation was set successfully. False, if not.
        :rtype: bool
        """
        father_sim_info = cls.get_father_sim_info(new_grandchild_sim_info)
        cls.set_as_mother_of(sim_info, father_sim_info)
        return True

    @classmethod
    def set_as_mothers_father_of(cls, sim_info: SimInfo, new_grandchild_sim_info: SimInfo) -> bool:
        """set_as_mothers_father_of(sim_info, new_grandchild_sim_info)

        Retrieve the Father of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param new_grandchild_sim_info: The new grandchild of Sim A.
        :type new_grandchild_sim_info: SimInfo
        :return: True, if the relation was set successfully. False, if not.
        :rtype: bool
        """
        mother_sim_info = cls.get_mother_sim_info(new_grandchild_sim_info)
        cls.set_as_father_of(sim_info, mother_sim_info)
        return True

    @classmethod
    def set_as_mothers_mother_of(cls, sim_info: SimInfo, new_grandchild_sim_info: SimInfo) -> bool:
        """set_as_mothers_mother_of(sim_info, new_grandchild_sim_info)

        Retrieve the Father of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :param new_grandchild_sim_info: The new grandchild of Sim A.
        :type new_grandchild_sim_info: SimInfo
        :return: True, if the relation was set successfully. False, if not.
        :rtype: bool
        """
        mother_sim_info = cls.get_mother_sim_info(new_grandchild_sim_info)
        cls.set_as_mother_of(sim_info, mother_sim_info)
        return True

    @classmethod
    def has_father(cls, sim_info: SimInfo) -> bool:
        """has_father(sim_info)

        Determine if a Sim has a father.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a father. False, if not.
        :rtype: bool
        """
        return cls.get_father_sim_info(sim_info) is not None

    @classmethod
    def has_mother(cls, sim_info: SimInfo) -> bool:
        """has_mother(sim_info)

        Determine if a Sim has a mother.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a mother. False, if not.
        :rtype: bool
        """
        return cls.get_mother_sim_info(sim_info) is not None

    @classmethod
    def has_mothers_mother(cls, sim_info: SimInfo) -> bool:
        """has_grandmother(sim_info)

        Determine if a Sim has a Grandmother on the Mother's side, otherwise known as the Mother's Mother.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a grandmother on the Mother's side. False, if not.
        :rtype: bool
        """
        return cls.get_mothers_mother_sim_info(sim_info) is not None

    @classmethod
    def has_mothers_father(cls, sim_info: SimInfo) -> bool:
        """has_mothers_father(sim_info)

        Determine if a Sim has a Grandfather on the Mother's side, otherwise known as the Mother's Father.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a grandfather on the Mother's side. False, if not.
        :rtype: bool
        """
        return cls.get_mothers_father_sim_info(sim_info) is not None

    @classmethod
    def has_fathers_mother(cls, sim_info: SimInfo) -> bool:
        """has_fathers_mother(sim_info)

        Determine if a Sim has a Grandmother on the Father's side, otherwise known as the Father's Mother.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a grandmother on the Father's side. False, if not.
        :rtype: bool
        """
        return cls.get_fathers_mother_sim_info(sim_info) is not None

    @classmethod
    def has_fathers_father(cls, sim_info: SimInfo) -> bool:
        """has_fathers_father(sim_info)

        Determine if a Sim has a Grandfather on the Father's side, otherwise known as the Father's Father.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a grandfather on the Father's side. False, if not.
        :rtype: bool
        """
        return cls.get_fathers_father_sim_info(sim_info) is not None

    @classmethod
    def has_children(cls, sim_info: SimInfo) -> bool:
        """has_children(sim_info)

        Determine if a Sim has any children.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has any children. False, if not.
        :rtype: bool
        """
        return any(cls.get_children_sim_info_gen(sim_info))

    @classmethod
    def get_father_sim_info(cls, sim_info: SimInfo) -> Union[SimInfo, None]:
        """get_father_sim_info(sim_info)

        Retrieve the Father of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The father of the Sim or None if the Sim does not have a father.
        :rtype: Union[SimInfo, None]
        """
        return CommonSimUtils.get_sim_info(cls._retrieve_parent_relation_sim_id(sim_info, FamilyRelationshipIndex.FATHER))

    @classmethod
    def get_mother_sim_info(cls, sim_info: SimInfo) -> Union[SimInfo, None]:
        """get_mother_sim_info(sim_info)

        Retrieve the Mother of a Sim.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The mother of the Sim or None if the Sim does not have a mother.
        :rtype: Union[SimInfo, None]
        """
        return CommonSimUtils.get_sim_info(cls._retrieve_parent_relation_sim_id(sim_info, FamilyRelationshipIndex.MOTHER))

    @classmethod
    def get_mothers_mother_sim_info(cls, sim_info: SimInfo) -> Union[SimInfo, None]:
        """get_mothers_mother_sim_info(sim_info)

        Retrieve the Grandmother of a Sim on their mothers side.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The grandmother of the Sim on their mothers side or None if the Sim does not have a mother or their mother does not have a mother.
        :rtype: Union[SimInfo, None]
        """
        mother_sim_info = cls.get_mother_sim_info(sim_info)
        if mother_sim_info is None:
            return None
        return cls.get_mother_sim_info(mother_sim_info)

    @classmethod
    def get_mothers_father_sim_info(cls, sim_info: SimInfo) -> Union[SimInfo, None]:
        """get_mothers_father_sim_info(sim_info)

        Retrieve the Grandfather of a Sim on their mothers side.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The grandfather of the Sim on their mothers side or None if the Sim does not have a mother or their mother does not have a father.
        :rtype: Union[SimInfo, None]
        """
        mother_sim_info = cls.get_mother_sim_info(sim_info)
        if mother_sim_info is None:
            return None
        return cls.get_father_sim_info(mother_sim_info)

    @classmethod
    def get_fathers_mother_sim_info(cls, sim_info: SimInfo) -> Union[SimInfo, None]:
        """get_fathers_mother_sim_info(sim_info)

        Retrieve the Grandmother of a Sim on their fathers side.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The grandmother of the Sim on their fathers side or None if the Sim does not have a father or their father does not have a mother.
        :rtype: Union[SimInfo, None]
        """
        father_sim_info = cls.get_father_sim_info(sim_info)
        if father_sim_info is None:
            return None
        return cls.get_mother_sim_info(father_sim_info)

    @classmethod
    def get_fathers_father_sim_info(cls, sim_info: SimInfo) -> Union[SimInfo, None]:
        """get_fathers_father_sim_info(sim_info)

        Retrieve the Grandfather of a Sim on their fathers side.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: The grandfather of the Sim on their fathers side or None if the Sim does not have a father or their father does not have a mother.
        :rtype: Union[SimInfo, None]
        """
        father_sim_info = cls.get_father_sim_info(sim_info)
        if father_sim_info is None:
            return None
        return cls.get_father_sim_info(father_sim_info)

    @classmethod
    def get_children_sim_info_gen(cls, sim_info: SimInfo) -> Iterator[SimInfo]:
        """get_children_sim_info_gen(sim_info)

        Get the blood related children of a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: An iterable of children the specified Sim is blood related to.
        :rtype: Iterator[SimInfo]
        """
        genealogy_tracker = cls.get_genealogy_tracker(sim_info)
        if genealogy_tracker is None:
            return tuple()
        for sim_id in genealogy_tracker.get_child_sim_infos_gen():
            child_sim_info = CommonSimUtils.get_sim_info(sim_id)
            if child_sim_info is not None:
                yield child_sim_info

    @classmethod
    def get_siblings_sim_info_gen(cls, sim_info: SimInfo) -> Iterator[SimInfo]:
        """get_siblings_sim_info_gen(sim_info)

        Get the blood related siblings of a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: An iterable of siblings the specified Sim is blood related to.
        :rtype: Iterator[SimInfo]
        """
        genealogy_tracker = cls.get_genealogy_tracker(sim_info)
        if genealogy_tracker is None:
            return tuple()
        for sim_id in genealogy_tracker.get_siblings_sim_infos_gen():
            sibling_sim_info = CommonSimUtils.get_sim_info(sim_id)
            if sibling_sim_info is not None:
                yield sibling_sim_info

    @classmethod
    def get_grandparent_sim_info_gen(cls, sim_info: SimInfo) -> Iterator[SimInfo]:
        """get_grandparent_sim_info_gen(sim_info)

        Get the blood related Grandparents of a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: An iterable of Grandparents the specified Sim is blood related to.
        :rtype: Iterator[SimInfo]
        """
        genealogy_tracker = cls.get_genealogy_tracker(sim_info)
        if genealogy_tracker is None:
            return tuple()
        for sim_id in genealogy_tracker.get_grandparent_sim_ids_gen():
            grandparent_sim_info = CommonSimUtils.get_sim_info(sim_id)
            if grandparent_sim_info is not None:
                yield grandparent_sim_info

    @classmethod
    def get_parent_sim_info_gen(cls, sim_info: SimInfo) -> Iterator[SimInfo]:
        """get_parent_sim_info_gen(sim_info)

        Get the blood related Parents of a Sim.

        :param sim_info: The info of a Sim.
        :type sim_info: SimInfo
        :return: An iterable of Parents the specified Sim is blood related to.
        :rtype: Iterator[SimInfo]
        """
        genealogy_tracker = cls.get_genealogy_tracker(sim_info)
        if genealogy_tracker is None:
            return tuple()
        for sim_id in genealogy_tracker.get_parent_sim_infos_gen():
            parent_sim_info = CommonSimUtils.get_sim_info(sim_id)
            if parent_sim_info is not None:
                yield parent_sim_info

    @classmethod
    def remove_family_relations_with(cls, sim_info_a: SimInfo, sim_info_b: SimInfo, remove_from_family_tree: bool = True) -> bool:
        """remove_family_relations_with(sim_info_a, sim_info_b, remove_from_family_tree=True)

        Remove the family relations Sim A has with Sim B and the family relations Sim B has with Sim A.

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: The Sim to remove from the family of Sim A.
        :type sim_info_b: SimInfo
        :param remove_from_family_tree: If True, Sim A will remove Sim B from their family tree as well. If False, the family tree of Sim A will not be modified. Default is True.
        :type remove_from_family_tree: bool, optional
        :return: True, if the family relations between the Sims was removed successfully. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_family_tree_utils import CommonSimFamilyTreeUtils
        family_tree_service = CommonSimFamilyTreeUtils.get_family_tree_service()
        if family_tree_service is not None:
            cls._remove_family_link(sim_info_a, sim_info_b)
            cls._remove_family_link(sim_info_b, sim_info_a)
            sim_id_a = CommonSimUtils.get_sim_id(sim_info_a)
            sim_id_b = CommonSimUtils.get_sim_id(sim_info_b)
            family_tree_service.clear_family_relations_between(sim_id_a, sim_id_b)
        return True

    @classmethod
    def remove_father_relation(cls, sim_info: SimInfo) -> bool:
        """remove_father_relation(sim_info)

        Remove the Father of a Sim from their Family Tree.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the father of the Sim has been removed. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_family_tree_utils import CommonSimFamilyTreeUtils
        family_tree_service = CommonSimFamilyTreeUtils.get_family_tree_service()
        if family_tree_service is not None:
            mother_sim_info = cls.get_mother_sim_info(sim_info)
            father_sim_info = cls.get_father_sim_info(sim_info)
            cls._remove_family_link(sim_info, father_sim_info)
            cls._remove_family_link(father_sim_info, sim_info)
            sim_id = CommonSimUtils.get_sim_id(sim_info)
            family_tree_service.clear_family_relation(sim_id, relationship_enum=FamilyRelationBitFlags.PARENT)
            cls.set_as_mother_of(mother_sim_info, sim_info)
        return True

    @classmethod
    def remove_mother_relation(cls, sim_info: SimInfo) -> bool:
        """remove_mother_relation(sim_info)

        Remove the Mother of a Sim from their Family Tree.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the mother of the Sim has been removed. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_family_tree_utils import CommonSimFamilyTreeUtils
        family_tree_service = CommonSimFamilyTreeUtils.get_family_tree_service()
        if family_tree_service is not None:
            father_sim_info = cls.get_father_sim_info(sim_info)
            mother_sim_info = cls.get_mother_sim_info(sim_info)
            cls._remove_family_link(sim_info, mother_sim_info)
            cls._remove_family_link(mother_sim_info, sim_info)
            sim_id = CommonSimUtils.get_sim_id(sim_info)
            family_tree_service.clear_family_relation(sim_id, relationship_enum=FamilyRelationBitFlags.PARENT)
            cls.set_as_father_of(father_sim_info, sim_info)
        return True

    @classmethod
    def remove_fathers_father_relation(cls, sim_info: SimInfo) -> bool:
        """remove_fathers_father_relation(sim_info)

        Remove the relation of a Sim to their Grandfather on their fathers side from their Family Tree.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the grandfather of the Sim has been removed. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_family_tree_utils import CommonSimFamilyTreeUtils
        family_tree_service = CommonSimFamilyTreeUtils.get_family_tree_service()
        if family_tree_service is not None:
            grandfather_sim_info = cls.get_fathers_father_sim_info(sim_info)
            cls._remove_family_link(sim_info, grandfather_sim_info)
            cls._remove_family_link(grandfather_sim_info, sim_info)
            father_sim_info = cls.get_father_sim_info(sim_info)
            cls.remove_father_relation(father_sim_info)
        return True

    @classmethod
    def remove_fathers_mother_relation(cls, sim_info: SimInfo) -> bool:
        """remove_fathers_mother_relation(sim_info)

        Remove the relation of a Sim to their Grandmother on their fathers side from their Family Tree.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the grandmother of the Sim has been removed. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_family_tree_utils import CommonSimFamilyTreeUtils
        family_tree_service = CommonSimFamilyTreeUtils.get_family_tree_service()
        if family_tree_service is not None:
            grandmother_sim_info = cls.get_fathers_father_sim_info(sim_info)
            cls._remove_family_link(sim_info, grandmother_sim_info)
            cls._remove_family_link(grandmother_sim_info, sim_info)
            father_sim_info = cls.get_father_sim_info(sim_info)
            cls.remove_mother_relation(father_sim_info)
        return True

    @classmethod
    def remove_mothers_father_relation(cls, sim_info: SimInfo) -> bool:
        """remove_mothers_father_relation(sim_info)

        Remove the Father of the Mother of a Sim from their Family Tree.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the father of the mother of the Sim has been removed. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_family_tree_utils import CommonSimFamilyTreeUtils
        family_tree_service = CommonSimFamilyTreeUtils.get_family_tree_service()
        if family_tree_service is not None:
            grandfather_sim_info = cls.get_mothers_father_sim_info(sim_info)
            cls._remove_family_link(sim_info, grandfather_sim_info)
            cls._remove_family_link(grandfather_sim_info, sim_info)
            mother_sim_info = cls.get_mother_sim_info(sim_info)
            cls.remove_father_relation(mother_sim_info)
        return True

    @classmethod
    def remove_mothers_mother_relation(cls, sim_info: SimInfo) -> bool:
        """remove_mothers_mother_relation(sim_info)

        Remove the relation of a Sim to their Grandmother on their mothers side from their Family Tree.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the grandmother of the Sim has been removed. False, if not.
        :rtype: bool
        """
        from sims4communitylib.utils.sims.common_sim_family_tree_utils import CommonSimFamilyTreeUtils
        family_tree_service = CommonSimFamilyTreeUtils.get_family_tree_service()
        if family_tree_service is not None:
            grandmother_sim_info = cls.get_mothers_mother_sim_info(sim_info)
            cls._remove_family_link(sim_info, grandmother_sim_info)
            cls._remove_family_link(grandmother_sim_info, sim_info)
            mother_sim_info = cls.get_mother_sim_info(sim_info)
            cls.remove_mother_relation(mother_sim_info)
        return True

    @classmethod
    def is_father_of(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """is_father_of(sim_info_a, sim_info_b)

        Determine if Sim A is the father of Sim B.

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: An instance of a Sim.
        :type sim_info_b: SimInfo
        :return: True, if Sim A is the father of Sim B. False, if not.
        :rtype: bool
        """
        parent_sim_info_b = cls.get_father_sim_info(sim_info_b)
        return sim_info_a is parent_sim_info_b

    @classmethod
    def is_mother_of(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """is_mother_of(sim_info_a, sim_info_b)

        Determine if Sim A is the mother of Sim B.

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: An instance of a Sim.
        :type sim_info_b: SimInfo
        :return: True, if Sim A is the mother of Sim B. False, if not.
        :rtype: bool
        """
        parent_sim_info_b = cls.get_mother_sim_info(sim_info_b)
        return sim_info_a is parent_sim_info_b

    @classmethod
    def is_fathers_father_of(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """is_fathers_father_of(sim_info_a, sim_info_b)

        Determine if Sim A is the grandfather of Sim B on the fathers side of Sim B.

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: An instance of a Sim.
        :type sim_info_b: SimInfo
        :return: True, if Sim A is the grandfather of Sim B on their fathers side. False, if not.
        :rtype: bool
        """
        grand_parent_sim_info_b = cls.get_fathers_father_sim_info(sim_info_b)
        return sim_info_a is grand_parent_sim_info_b

    @classmethod
    def is_fathers_mother_of(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """is_fathers_mother_of(sim_info_a, sim_info_b)

        Determine if Sim A is the grandmother of Sim B on the fathers side of Sim B.

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: An instance of a Sim.
        :type sim_info_b: SimInfo
        :return: True, if Sim A is the grandmother of Sim B on their fathers side. False, if not.
        :rtype: bool
        """
        grand_parent_sim_info_b = cls.get_fathers_mother_sim_info(sim_info_b)
        return sim_info_a is grand_parent_sim_info_b

    @classmethod
    def is_mothers_father_of(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """is_mothers_father_of(sim_info_a, sim_info_b)

        Determine if Sim A is the grandfather of Sim B on the mothers side of Sim B.

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: An instance of a Sim.
        :type sim_info_b: SimInfo
        :return: True, if Sim A is the grandfather of Sim B on their mothers side. False, if not.
        :rtype: bool
        """
        grand_parent_sim_info_b = cls.get_mothers_father_sim_info(sim_info_b)
        return sim_info_a is grand_parent_sim_info_b

    @classmethod
    def is_mothers_mother_of(cls, sim_info_a: SimInfo, sim_info_b: SimInfo) -> bool:
        """is_mothers_mother_of(sim_info_a, sim_info_b)

        Determine if Sim A is the grandmother of Sim B on the mothers side of Sim B.

        :param sim_info_a: An instance of a Sim.
        :type sim_info_a: SimInfo
        :param sim_info_b: An instance of a Sim.
        :type sim_info_b: SimInfo
        :return: True, if Sim A is the grandmother of Sim B on their mothers side. False, if not.
        :rtype: bool
        """
        grand_parent_sim_info_b = cls.get_mothers_mother_sim_info(sim_info_b)
        return sim_info_a is grand_parent_sim_info_b

    @classmethod
    def has_grandfather_on_fathers_side(cls, sim_info: SimInfo) -> bool:
        """has_grandfather_on_fathers_side(sim_info)

        Determine if a Sim has a grandfather on the fathers side.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a grandfather on the fathers side. False, if not.
        :rtype: bool
        """
        return cls.get_fathers_father_sim_info(sim_info) is not None

    @classmethod
    def has_grandmother_on_fathers_side(cls, sim_info: SimInfo) -> bool:
        """has_grandmother_on_fathers_side(sim_info)

        Determine if a Sim has a grandmother on the fathers side.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a grandmother on the fathers side. False, if not.
        :rtype: bool
        """
        return cls.get_fathers_mother_sim_info(sim_info) is not None

    @classmethod
    def has_grandfather_on_mothers_side(cls, sim_info: SimInfo) -> bool:
        """has_grandfather_on_mothers_side(sim_info)

        Determine if a Sim has a grandfather on the mothers side.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a grandfather on the mothers side. False, if not.
        :rtype: bool
        """
        return cls.get_mothers_father_sim_info(sim_info) is not None

    @classmethod
    def has_grandmother_on_mothers_side(cls, sim_info: SimInfo) -> bool:
        """has_grandmother_on_mothers_side(sim_info)

        Determine if a Sim has a grandmother on the mothers side.

        :param sim_info: An instance of a Sim.
        :type sim_info: SimInfo
        :return: True, if the Sim has a grandmother on the mothers side. False, if not.
        :rtype: bool
        """
        return cls.get_mothers_mother_sim_info(sim_info) is not None

    @classmethod
    def _remove_family_link(cls, sim_info_a: SimInfo, sim_info_b: SimInfo):
        bit = sim_info_a.genealogy.get_family_relationship_bit(sim_info_b.id)
        if bit is None:
            return False
        source_relationship_tracker = sim_info_a.relationship_tracker
        if source_relationship_tracker.has_bit(sim_info_b.id, bit):
            return True
        source_relationship_tracker.remove_relationship_bit(sim_info_b.id, bit, from_load=False)
        if RelationshipGlobalTuning.ROMANCE_BIT_NOT_FOR_FAMILY is not None and bit != TropeGlobalTuning.RELATIONSHIP_TYPE_TO_BIT[RelationshipType.SPOUSE] and not source_relationship_tracker.has_bit(sim_info_b.id, RelationshipGlobalTuning.ROMANCE_BIT_NOT_FOR_FAMILY):
            source_relationship_tracker.add_relationship_bit(sim_info_b.id, RelationshipGlobalTuning.ROMANCE_BIT_NOT_FOR_FAMILY)
        return True

    @classmethod
    def _retrieve_parent_relation_sim_id(cls, sim_info: SimInfo, relationship_index: FamilyRelationshipIndex) -> Union[SimInfo, None]:
        genealogy_tracker = cls.get_genealogy_tracker(sim_info)
        if genealogy_tracker is None:
            return None
        if relationship_index not in genealogy_tracker._family_relations:
            return None
        sim_id = genealogy_tracker.get_parent_relation(relationship_index, allow_invalid_parent=True)
        if sim_id is None:
            return None
        return CommonSimUtils.get_sim_info(sim_id)
