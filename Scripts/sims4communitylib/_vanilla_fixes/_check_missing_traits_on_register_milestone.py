"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) DEVIANTGAMEMODS
"""
from typing import Any

from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from situations.situation_goal_actor import SituationGoalActorTrait


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SituationGoalActorTrait, '_register_events', handle_exceptions=False)
def _common_fix_issue_when_checking_register_missing_traits(original, self, *_, **__) -> Any:
    new_whitelist_traits = list()
    for trait in self._goal_test.whitelist_traits:
        if trait is not None:
            new_whitelist_traits.append(trait)
    self._goal_test.whitelist_traits = list(new_whitelist_traits)
    return original(self, *_, **__)


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SituationGoalActorTrait, '_unregister_events', handle_exceptions=False)
def _common_fix_issue_when_checking_unregister_missing_traits(original, self, *_, **__) -> Any:
    new_whitelist_traits = list()
    for trait in self._goal_test.whitelist_traits:
        if trait is not None:
            new_whitelist_traits.append(trait)
    self._goal_test.whitelist_traits = list(new_whitelist_traits)
    return original(self, *_, **__)
