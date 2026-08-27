"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) DEVIANTGAMEMODS
"""
import services
from filters.tunable import TunableAggregateFilter, FilterTermTag
from sims4.resources import Types
from sims4.tuning.tunable import TunableTuple, TunableReference, TunableEnumEntry, TunableList, Tunable
from sims4communitylib.classes.testing.common_test_set_instance import S4CLTunableTestSet


class CommonTunableAggregateSimFilter(TunableAggregateFilter):
    """Aggregate filter with Sim tests to check Sim validity."""
    INSTANCE_TUNABLES = {
        'leader_filter': TunableTuple(
            filter=TunableReference(
                description='\n                Sim filter that is used as the leader of the group. All\n                relationships will use this sim as the reference point.\n                ',
                manager=services.get_instance_manager(Types.SIM_FILTER),
                class_restrictions=('CommonTunableSimFilter', 'TunableSimFilter')
            ),
            tag=TunableEnumEntry(
                description='\n                Tag associated with the filter which allows for specific filters\n                to be associated with specific things, like which job to apply\n                to the Sim with that filter.\n                ',
                tunable_type=FilterTermTag,
                default=FilterTermTag.NO_TAG
            )
        ),
        'filters': TunableList(
            description='\n            List of filters for the sims to be included in the group.\n            ',
            tunable=TunableTuple(
                filter=TunableReference(
                    manager=services.get_instance_manager(Types.SIM_FILTER),
                    class_restrictions=('CommonTunableSimFilter', 'TunableSimFilter')
                ),
                tag=TunableEnumEntry(
                    description='\n                    Tag associated with the filter which allows for specific filters\n                    to be associated with specific things, like which job to apply\n                    to the Sim with that filter.\n                    ',
                    tunable_type=FilterTermTag,
                    default=FilterTermTag.NO_TAG
                ),
                optional=Tunable(
                    description='\n                    Whether or not this filter is required for the filter to\n                    be considered successful.\n                    ',
                    tunable_type=bool,
                    default=True
                )
            )
        ),
        'sim_tests': S4CLTunableTestSet(
            description='\n                Tests that determine if a Sim from the filters can be chosen. If a Sim passes these tests, they can be chosen.'
        )
    }
