"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) DEVIANTGAMEMODS
"""
from typing import Any

from careers.career_base import CareerBase
from sims4communitylib.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

log = CommonLogRegistry().register_log(ModInfo.get_identity(), 's4cl_career_add_performance_statistic')


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), CareerBase, '_add_performance_statistics', handle_exceptions=False)
def _common_fix_fix_add_performance_statistics(original, self, *_, **__) -> Any:
    tuning = self.current_level_tuning
    sim_info = self._sim_info
    tracker = sim_info.get_tracker(tuning.performance_stat)
    if tracker is None:
        log.format_error_with_message(f'Failed to add performance statistic to {sim_info}, missing a tracker for performance statistic {tuning.performance_stat}')
        return
    tracker.add_statistic(tuning.performance_stat)
    for metric in tuning.performance_metrics.statistic_metrics:
        tracker = sim_info.get_tracker(metric.statistic)
        if tracker is None:
            log.format_error_with_message(f'Failed to add performance statistic to {sim_info}, missing a tracker for performance metrics statistic {metric.statistic}')
            continue
        tracker.add_statistic(metric.statistic)
