"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) DEVIANTGAMEMODS
"""
from event_testing.resolver import SingleSimResolver, DoubleSimResolver
from filters.tunable import FilterTermVariant, BaseFilterTerm, FilterResult
from sims.sim_info import SimInfo
from sims4communitylib.classes.testing.common_test_set_instance import CommonTunableTestSet
from sims4communitylib.logging._has_s4cl_log import _HasS4CLLog


class CommonTestSetFilterTerm(BaseFilterTerm, _HasS4CLLog):
    """CommonTestSetInstanceFilterTerm()

    A filter term that is used to filter items.
    """
    FACTORY_TUNABLES = {
        'tests': CommonTunableTestSet(
            description='Tests to run on Sims.'
        ),
    }

    __slots__ = {'tests'}

    # noinspection PyMissingOrEmptyDocstring
    @property
    def log_identifier(self) -> str:
        return 'common_filter_term'

    def __init__(self, *_, **__) -> None:
        super().__init__(*_, **__)
        _HasS4CLLog.__init__(self)

    # noinspection PyMissingOrEmptyDocstring
    @property
    def is_sim_info_conformable(self) -> bool:
        return False

    # noinspection PyMissingOrEmptyDocstring
    def calculate_score(self, sim_info, requesting_sim_info: SimInfo = None, **kwargs):
        score = 0
        if self.tests is None or not self.tests:
            self.log.format_with_message('No tests found.', sim=sim_info, requesting_sim_info=requesting_sim_info)
            return FilterResult(score=1, sim_info=sim_info)

        if requesting_sim_info is not None:
            resolver = DoubleSimResolver(sim_info, requesting_sim_info)
        else:
            resolver = SingleSimResolver(sim_info)
        if self.tests.run_tests(resolver):
            self.log.format_with_message('Tests passed', sim=sim_info, requesting_sim_info=requesting_sim_info)
            score = 1
        else:
            self.log.format_with_message('Tests failed', sim=sim_info, requesting_sim_info=requesting_sim_info)
        return FilterResult(score=score, sim_info=sim_info)

    # noinspection PyMissingOrEmptyDocstring
    def conform_sim_creator_to_filter_term(self, sim_creator=None, requesting_sim_info=None, **kwargs) -> FilterResult:
        return FilterResult.FALSE

    # noinspection PyMissingOrEmptyDocstring
    def conform_sim_info_to_filter_term(self, created_sim_info, sim_creator=None, requesting_sim_info=None, **kwargs) -> FilterResult:
        return FilterResult.FALSE


class CommonFilterTermVariant(FilterTermVariant):
    """CommonFilterTermVariant

    A filter term variant for adding custom filter terms to a filter.
    """

    def __init__(self, conform_optional=False, **kwargs) -> None:
        filter_kwargs = {}
        if conform_optional:
            filter_kwargs['conform_optional'] = True
        super().__init__(conform_optional=conform_optional, test_set=CommonTestSetFilterTerm.TunableFactory(**filter_kwargs), **kwargs)
