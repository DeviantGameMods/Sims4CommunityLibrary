"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) DEVIANTGAMEMODS
"""
from typing import Optional, Tuple, Any

from filters.tunable import TunableSimFilter, FilterResult
from event_testing.resolver import SingleSimResolver, DoubleSimResolver
from sims.sim_info import SimInfo
from sims4.tuning.tunable import TunableList
from sims4.utils import blueprintmethod
from sims4communitylib.classes.filters.common_filter_term_variant import CommonFilterTermVariant
from sims4communitylib.classes.testing.common_test_set_instance import S4CLTunableTestSet
from sims4communitylib.logging._has_s4cl_class_log import _HasS4CLClassLog


class CommonTunableSimFilter(TunableSimFilter, _HasS4CLClassLog):
    """A tunable Sim filter that properly filters Sims by using Tests to check Sim validity."""
    INSTANCE_TUNABLES = {
        '_filter_terms': TunableList(
            description='\n            A list of filter terms that will be used to query the townie pool\n            for sims.\n            ',
            tunable=CommonFilterTermVariant()
        ),
        'sim_tests': S4CLTunableTestSet(
            description='\n                Tests that determine if a Sim from the filter can be chosen.'
        ),
    }

    __slots__ = {'sim_tests'}

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 'common_tunable_sim_filter'

    def __init__(self, *_, **__) -> None:
        super().__init__(*_, **__)
        _HasS4CLClassLog.__init__(self)

    @blueprintmethod
    def _repurpose_sim_info(self, sim_info: SimInfo, additional_filter_terms: Tuple[Any] = (), requesting_sim_info: SimInfo = None, **kwargs) -> Optional[FilterResult]:
        if self.sim_tests is not None:
            if requesting_sim_info is not None:
                resolver = DoubleSimResolver(sim_info, requesting_sim_info)
            else:
                resolver = SingleSimResolver(sim_info)
            self.log.format_with_message('Repurposing Sim with tests', sim=sim_info, requesting_sim_info=requesting_sim_info)
            test_result = self.sim_tests.run_tests(resolver)
            if not test_result:
                self.log.format_with_message('Failed Sim Tests', sim=sim_info, result=test_result)
                return FilterResult(f'Failed Sim Tests {test_result}', score=0)

        return super()._repurpose_sim_info(sim_info, additional_filter_terms=additional_filter_terms, requesting_sim_info=requesting_sim_info, **kwargs)

    # noinspection PyMissingOrEmptyDocstring
    @blueprintmethod
    def create_sim_info(self, *args, requesting_sim_info: SimInfo = None, **kwargs) -> FilterResult:
        result = super().create_sim_info(*args, requesting_sim_info=requesting_sim_info, **kwargs)
        if self.sim_tests is not None:
            self.log.format_with_message('Creating Sim Info with Sim Tests', sim=result.sim_info, requesting_sim_info=requesting_sim_info)
            if requesting_sim_info is not None:
                resolver = DoubleSimResolver(result.sim_info, requesting_sim_info)
            else:
                resolver = SingleSimResolver(result.sim_info)
            test_result = self.sim_tests.run_tests(resolver)
            if not test_result:
                self.log.format_with_message('Failed Sim Tests', sim=result.sim_info, result=test_result)
                return FilterResult(f'Failed Sim Tests {test_result}', score=0)
        return result
