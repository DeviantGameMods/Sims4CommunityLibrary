"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) DEVIANTGAMEMODS
"""
import os
from typing import Union, Any, Iterator, Tuple

from interactions.base.interaction import Interaction
from interactions.constraints import Constraint
from interactions.context import InteractionContext
from interactions.interaction_finisher import FinishingType
from native.animation import NativeAsm
from postures.posture_state import PostureState
from protocolbuffers.Localization_pb2 import LocalizedString
from scheduling import Timeline
from sims.sim import Sim
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from singletons import DEFAULT

ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

if ON_RTD:
    class ParticipantType:
        Invalid = 0
        Actor = 1
        Object = 2
        TargetSim = 4
        Listeners = 8
        All = 16
        AllSims = 32
        Lot = 64
        CraftingProcess = 128
        JoinTarget = 256
        CarriedObject = 512
        Affordance = 1024
        InteractionContext = 2048
        CustomSim = 4096
        AllRelationships = 8192
        CraftingObject = 16384
        ActorSurface = 32768
        ObjectChildren = 65536
        LotOwners = 131072
        CreatedObject = 262144
        PickedItemId = 524288
        StoredSim = 1048576
        PickedObject = 2097152
        SocialGroup = 4194304
        OtherSimsInteractingWithTarget = 8388608
        PickedSim = 16777216
        ObjectParent = 33554432
        SignificantOtherActor = 67108864
        SignificantOtherTargetSim = 134217728
        OwnerSim = 268435456
        StoredSimOnActor = 536870912
        Unlockable = 1073741824
        LiveDragActor = 2147483648
        LiveDragTarget = 4294967296
        PickedZoneId = 8589934592
        SocialGroupSims = 17179869184
        PregnancyPartnerActor = 34359738368
        PregnancyPartnerTargetSim = 68719476736
        SocialGroupAnchor = 137438953472
        TargetSurface = 274877906944
        ActiveHousehold = 549755813888
        ActorPostureTarget = 1099511627776
        InventoryObjectStack = 2199023255552
        AllOtherInstancedSims = 4398046511104
        CareerEventSim = 8796093022208
        StoredSimOnPickedObject = 17592186044416
        SavedActor1 = 35184372088832
        SavedActor2 = 70368744177664
        SavedActor3 = 140737488355328
        SavedActor4 = 281474976710656
        LotOwnerSingleAndInstanced = 562949953421312
        LinkedPostureSim = 1125899906842624
        AssociatedClub = 2251799813685248
        AssociatedClubMembers = 4503599627370496
        AssociatedClubLeader = 9007199254740992
        AssociatedClubGatheringMembers = 18014398509481984
        ActorEnsemble = 36028797018963968
        TargetEnsemble = 72057594037927936
        TargetSimPostureTarget = 144115188075855872
        ActorEnsembleSansActor = 288230376151711744
        ActorDiningGroupMembers = 576460752303423488
        TableDiningGroupMembers = 1152921504606846976
        StoredSimOrNameData = 2305843009213693952
        TargetDiningGroupMembers = 4611686018427387904
        LinkedObjects = 9223372036854775808
        RoutingMaster = 18446744073709551616
        RoutingSlaves = 36893488147419103232
        SituationParticipants1 = 73786976294838206464
        SituationParticipants2 = 147573952589676412928
        ObjectCrafter = 295147905179352825856
        MissingPet = 590295810358705651712
        TargetTeleportPortalObjectDestinations = 1180591620717411303424
        ActorFeudTarget = 2361183241434822606848
        TargetFeudTarget = 4722366482869645213696
        ActorSquadMembers = 9444732965739290427392
        TargetSquadMembers = 18889465931478580854784
        AllInstancedSims = 37778931862957161709568
        StoredObjectsOnActor = 75557863725914323419136
        StoredObjectsOnTarget = 151115727451828646838272
        ObjectInventoryOwner = 302231454903657293676544
        LotOwnersOrRenters = 604462909807314587353088
        ActorFiance = 1208925819614629174706176
        TargetFiance = 2417851639229258349412352
        RandomInventoryObject = 4835703278458516698824704
        SituationParticipants3 = 9671406556917033397649408
        Familiar = 19342813113834066795298816
        ObjectProvidingTargetAffordance = 38685626227668133590597632
        StoredSimOnObjectProvidingTargetAffordance = 77371252455336267181195264
        PhotographyTargets = 154742504910672534362390528
        FamiliarOfTarget = 309485009821345068724781056
        PickedStatistic = 618970019642690137449562112
        ActorHousehold = 1237940039285380274899124224
        TargetHousehold = 2475880078570760549798248448
        AllInstancedActiveHouseholdSims = 4951760157141521099596496896
        Street = 9903520314283042199192993792
        VenuePolicyProvider = 19807040628566084398385987584
        ActorLot = 39614081257132168796771975168
        ObjectIngredients = 79228162514264337593543950336
        CreatedObjectIngredients = 158456325028528675187087900672
        StoredCASPartsOnObject = 316912650057057350374175801344
        RoutingOwner = 633825300114114700748351602688
        RoutingTarget = 1267650600228229401496703205376
        CurrentRegion = 2535301200456458802993406410752
        ActorLotLevel = 5070602400912917605986812821504
        ObjectLotLevel = 10141204801825835211973625643008
        TargetHouseholdMembers = 20282409603651670423947251286016
        ObjectAnimalHome = 40564819207303340847894502572032
        AnimalHomeAssignees = 81129638414606681695789005144064
        SituationCraftingItem = 162259276829213363391578010288128
        ObjectRelationshipsComponent = 324518553658426726783156020576256
        ActorHouseholdMembers = 649037107316853453566312041152512
        SavedStoryProgressionSim1 = 1298074214633706907132624082305024
        SavedStoryProgressionSim2 = 2596148429267413814265248164610048
        SavedStoryProgressionZone1 = 5192296858534827628530496329220096
        SavedStoryProgressionZone2 = 10384593717069655257060992658440192
        SavedStoryProgressionString1 = 20769187434139310514121985316880384
        SavedStoryProgressionString2 = 41538374868278621028243970633760768
        SavedStoryProgressionString3 = 83076749736557242056487941267521536
        SavedStoryProgressionString4 = 166153499473114484112975882535043072
        SavedStoryProgressionString5 = 332306998946228968225951765070086144
        ActorClanLeader = 664613997892457936451903530140172288
        TargetClanLeader = 1329227995784915872903807060280344576
        ObjectTrendiOutfitTrend = 2658455991569831745807614120560689152
        ObjectTrendiOutfitTrendTag = 5316911983139663491615228241121378304
        GraduatesCurrent = 10633823966279326983230456482242756608
        GraduatesWaiting = 21267647932558653966460912964485513216
        FashionTrends = 42535295865117307932921825928971026432
        CarryCancellationOriginatorTarget = 85070591730234615865843651857942052864
        TargetSimFrontCarriedSim = 170141183460469231731687303715884105728
        TargetSimBackCarriedSim = 1 << 128
        CarriedSim = 1 << 129
        PurchasedObject = 1 << 130
        StoredSimOrNameDataList = 1 << 131
        StoredSim2 = 1 << 132
        ActorBassinet = 1 << 133
        TargetBassinet = 1 << 134
        ObjectAnimalCost = 1 << 135
        TargetObjectOfJoinedInteraction = 1 << 136
        ObjectAnimalCurrentValue = 1 << 137
        ActorPropertyOwners = 1 << 138
        ActorPropertyOwnerHousehold = 1 << 139
        ActorTenants = 1 << 140
        ActorTenantHouseholds = 1 << 141
        ActorZoneId = 1 << 142
        TargetSimZoneId = 1 << 143
        RandomZoneId = 1 << 144
        AllUnitZoneIds = 1 << 145
        CurrentZoneId = 1 << 146
        PickedZoneHouseholdSims = 1 << 147
        AllSimsInCurrentGame = 1 << 148
        OtherSimsInCurrentGame = 1 << 149
        AllSignificantOthersActor = 1 << 150
        AllSignificantOthersTargetSim = 1 << 151
        HeirloomCreatorSim = 1 << 152
        CurrentlyOpenSmallBusinessOwner = 1 << 153
        SmallBusinessEmployees = 1 << 154
        StoredPickedTattooOnActor = 1 << 155
        StoredPickedTattooOnTarget = 1 << 156
        ActorImaginaryFriend = 1 << 157
        ImaginaryFriendChild = 1 << 158
        GetawaySimsOfInterest = 1 << 159
        GetawayEliminationCandidates = 1 << 160
        PickedSecret = 1 << 161
        AllNoblesInCurrentNeighborhood = 1 << 162
        AllNoblesInActorNeighborhood = 1 << 163
        ActorDynastyHead = 1 << 164
        ActorDynastyHeir = 1 << 165
        ActorDynastyMembers = 1 << 166
        TargetDynastyHead = 1 << 167
        TargetDynastyHeir = 1 << 168
        TargetDynastyMembers = 1 << 169
        PreBlackmailedSecret = 1 << 170
        PreBlackmailerSim = 1 << 171
        KingdomPrimarySimFromActor = 1 << 172
        KingdomPrimarySimFromTarget = 1 << 173
        PickedSecretOwner = 1 << 174
else:
    from interactions import ParticipantType


class _CommonInteractionHooksMixin:
    """Hooks that are called from the various custom interactions."""

    # The following functions are hooks into various parts of an interaction override them in your own interaction to provide custom functionality.

    # noinspection PyUnusedLocal
    @classmethod
    def on_replacement_constraints_gen(cls, inst_or_cls: 'Interaction', sim: Sim, target: Any) -> Union[Iterator[Constraint], None]:
        """on_replacement_constraints_gen(inst_or_cls, sim, target)

        A hook that occurs before the normal constraints of an interaction, these constraints will replace the normal constraints of the interaction.

        .. note:: If None is returned, the normal constraints will be used. (Plus any additional constraints from on_constraint_gen)

        :param inst_or_cls: An instance or the class of the interaction.
        :type inst_or_cls: Interaction
        :param sim: The source Sim of the interaction.
        :type sim: Sim
        :param target: The target Object of the interaction.
        :type target: Any
        :return: An iterator of constraints to replace the normal constraints of the interaction or None if replacement constraints are not wanted.
        :rtype: Union[Iterator[Constraint], None]
        """
        return None

    # noinspection PyUnusedLocal
    @classmethod
    def on_constraint_gen(cls, inst_or_cls: 'Interaction', sim: Sim, target: Any) -> Union[Iterator[Constraint], Constraint, None]:
        """on_constraint_gen(inst_or_cls, sim, target)

        A hook that occurs after generating the constraints of an interaction, this constraint will be returned in addition to the normal constraints of the interaction.

        .. note:: Return None from this function to exclude any custom constraints.

        :param inst_or_cls: An instance or the class of the interaction.
        :type inst_or_cls: Interaction
        :param sim: The source Sim of the interaction.
        :type sim: Sim
        :param target: The target Object of the interaction.
        :type target: Any
        :return: A constraint or an iterator of constraints to return in addition to the normal constraints or None if no additional constraints should be added.
        :rtype: Union[Iterator[Constraint], Constraint, None]
        """
        return None

    # noinspection PyUnusedLocal
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, *args, **kwargs) -> CommonTestResult:
        """on_test(interaction_sim, interaction_target, interaction_context, *args, **kwargs)

        A hook that occurs upon the interaction being tested for availability.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param interaction_context: The context of the interaction.
        :type interaction_context: InteractionContext
        :return: The outcome of testing the availability of the interaction
        :rtype: CommonTestResult
        """
        return CommonTestResult.TRUE

    # noinspection PyUnusedLocal
    @classmethod
    def on_post_super_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, *args, **kwargs) -> CommonTestResult:
        """on_post_super_test(interaction_sim, interaction_target, interaction_context, *args, **kwargs)

        A hook that occurs after the interaction being tested for availability by on_test and the super _test functions.

        .. note:: This will only run if both on_test and _test returns CommonTestResult.TRUE or similar.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param interaction_context: The context of the interaction.
        :type interaction_context: InteractionContext
        :return: The outcome of testing the availability of the interaction
        :rtype: CommonTestResult
        """
        return CommonTestResult.TRUE

    # noinspection PyUnusedLocal
    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> CommonExecutionResult:
        """on_started(interaction_sim, interaction_target)

        A hook that occurs upon the interaction being started.

        .. note:: If CommonExecutionResult.FALSE, CommonExecutionResult.NONE, or False is returned from here, then the interaction will be cancelled instead of starting.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :return: The result of running the start function. True, if the interaction hook was executed successfully. False, if the interaction hook was not executed successfully.
        :rtype: CommonExecutionResult
        """
        return CommonExecutionResult.TRUE

    # noinspection PyUnusedLocal
    def on_killed(self, interaction_sim: Sim, interaction_target: Any) -> None:
        """on_killed(interaction_sim, interaction_target)

        A hook that occurs upon the interaction being killed.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :return: True, if the interaction hook was executed successfully. False, if the interaction hook was not executed successfully.
        :rtype: bool
        """
        if hasattr(self, 'verbose_log'):
            self.verbose_log.format_with_message('on_killed', sim=interaction_sim, target=interaction_target, interaction=self)

    def on_cancelled(self, interaction_sim: Sim, interaction_target: Any, finishing_type: FinishingType, cancel_reason_msg: str, *args, **kwargs) -> None:
        """on_cancelled(interaction_sim, interaction_target, finishing_type, cancel_reason_msg, *args, **kwargs)

        A hook that occurs upon the interaction being cancelled.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param finishing_type: The type of cancellation of the interaction.
        :type finishing_type: FinishingType
        :param cancel_reason_msg: The reason the interaction was cancelled.
        :type cancel_reason_msg: str
        """
        if hasattr(self, 'verbose_log'):
            self.verbose_log.format_with_message('on_cancelled', sim=interaction_sim, target=interaction_target, interaction=self, cancel_reason_msg=cancel_reason_msg, finishing_type=finishing_type, interaction_target=interaction_target, argles=args, kwargles=kwargs)

    def _on_reset(self, interaction_sim: Sim, interaction_target: Any) -> None:
        """_on_reset(interaction_sim, interaction_target)

        A hook that occurs upon the interaction being reset.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        """
        if hasattr(self, 'verbose_log'):
            self.verbose_log.format_with_message('on reset', sim=interaction_sim, target=interaction_target, interaction=self)

    def on_performed(self, interaction_sim: Sim, interaction_target: Any) -> None:
        """on_performed(interaction_sim, interaction_target)

        A hook that occurs after the interaction has been performed.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        """
        if hasattr(self, 'verbose_log'):
            self.verbose_log.format_with_message('on_performed', sim=interaction_sim, target=interaction_target, interaction=self)

    # noinspection PyUnusedLocal
    @classmethod
    def get_custom_replacement_participants(cls, participant_type: ParticipantType, sim: Union[Sim, None], target: Union[Sim, None], carry_target: Union[Any, None], interaction: 'Interaction'=None, **kwargs) -> Union[Tuple[Any], None]:
        """get_custom_replacement_participants(participant_type, sim=None, target=None, carry_target=None, interaction=None, **kwargs)

        A hook used to replace the result of the get_participants function with custom participants.

        :param participant_type: The type of participant being searched for.
        :type participant_type: ParticipantType
        :param sim: The Source of the interaction.
        :type sim: Union[Sim, None]
        :param target: The Target of the interaction.
        :type sim: Union[Sim, None]
        :param carry_target: The target being carried while the interaction is being run.
        :type carry_target: Union[Any, None]
        :param interaction: An instance of the interaction, if get_participants was invoked using an instance or None if get_participants was invoked using the class. Default is None.
        :type interaction: Interaction, optional
        :return: A collection of custom participants to use as replacements for the normal result of get_participants. Return None to keep the original participants. Default return is None.
        :rtype: Union[Tuple[Any], None]
        """
        return None

    # noinspection PyUnusedLocal
    @classmethod
    def get_custom_participants(cls, participant_type: ParticipantType, sim: Union[Sim, None], target: Union[Sim, None], carry_target: Union[Any, None], interaction: 'Interaction'=None, **kwargs) -> Tuple[Any]:
        """get_custom_participants(participant_type, sim=None, target=None, carry_target=None, interaction=None, **kwargs)

        A hook used to add custom participants to the result of the get_participants function.

        :param participant_type: The type of participant being searched for.
        :type participant_type: ParticipantType
        :param sim: The Source of the interaction.
        :type sim: Union[Sim, None]
        :param target: The Target of the interaction.
        :type sim: Union[Sim, None]
        :param carry_target: The target being carried while the interaction is being run.
        :type carry_target: Union[Any, None]
        :param interaction: An instance of the interaction, if get_participants was invoked using an instance or None if get_participants was invoked using the class. Default is None.
        :type interaction: Interaction, optional
        :return: A collection of custom participants to add to the normal result of get_participants.
        :rtype: Tuple[Any]
        """
        return tuple()

    def modify_posture_state(self, posture_state: PostureState, participant_type: ParticipantType = ParticipantType.Actor, sim: Sim = DEFAULT) -> Tuple[PostureState, ParticipantType, Sim]:
        """modify_posture_state(posture_state, participant_type=ParticipantType.Actor, sim=DEFAULT)

        A hook that allows modification of the posture state of the interactions participants.

        :param posture_state: The posture state being modified.
        :type posture_state: PostureState
        :param participant_type: The position in the interaction that the `sim` is considered at. Example: `ParticipantType.Actor` represents the source Sim of the interaction.
        :type participant_type: ParticipantType, optional
        :param sim: The Sim the posture state is being applied to.
        :type sim: Sim, optional
        :return: Return a modified PostureState, ParticipantType, and Sim.
        :rtype: Tuple[PostureState, ParticipantType, Sim]
        """
        return posture_state, participant_type, sim

    @classmethod
    def _create_override_display_name(
        cls,
        interaction_sim: Sim,
        interaction_target: Any,
        interaction: 'Interaction' = None,
        interaction_context: InteractionContext = None,
        **interaction_parameters
    ) -> Union[LocalizedString, None]:
        """_create_override_display_name(\
            interaction_sim,\
            interaction_target,\
            interaction=None,\
            interaction_context=None,\
            **interaction_parameters\
        )

        If overridden you may supply a custom name for the interaction to display.

        .. warning:: The returned value from here replaces the original returned value. Return None from here to return the original value.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param interaction: The interaction being performed or None.
        :type interaction: Interaction
        :param interaction_context: The context of the interaction being performed or None.
        :type interaction_context: InteractionContext
        :param interaction_parameters: Parameters for the interaction.
        :type interaction_parameters: Iterator[Any]
        :return: The name to use in place of the original name of the interaction or None if you want the original name to be used.
        :rtype: Union[LocalizedString, None]
        """
        pass

    # noinspection PyUnusedLocal
    def _setup_asm_default(self, interaction_sim: Sim, interaction_target: Any, interaction_asm: NativeAsm, *args, **kwargs) -> Union[bool, None]:
        """_setup_asm_default(interaction_sim, interaction_target, asm, *args, **kwargs)

        A hook that occurs upon the animation state machine being setup for the interaction.

        .. warning:: The returned value from here replaces the original returned value. Return None from here to return the original value.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param interaction_asm: An instance of an Animation State Machine
        :type interaction_asm: NativeAsm
        :return: True, if the ASM was setup properly. False, if not. or None to run through the original code.
        :rtype: bool
        """
        return None

    # noinspection PyUnusedLocal
    def _send_current_progress(self, interaction_sim: Sim, interaction_target: Any, *args, **kwargs) -> Union[bool, None]:
        """_send_current_progress(interaction_sim, interaction_target, *args, **kwargs)

        A hook that occurs upon sending the current progress for the interaction.

        .. warning:: The returned value from here replaces the original returned value.

        :param interaction_sim: The source Sim of the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :return: True, if progress was sent successfully. False, if not. Return None to run the original code.
        :rtype: bool
        """
        return None

    # noinspection PyUnusedLocal
    def on_run(self, interaction_sim: Sim, interaction_target: Any, timeline: Timeline):
        """on_run(interaction_sim, interaction_target, timeline)

        A hook that occurs upon the interaction being run.

        :param interaction_sim: The sim performing the interaction.
        :type interaction_sim: Sim
        :param interaction_target: The target of the interaction.
        :type interaction_target: Any
        :param timeline: The timeline the interaction is running on.
        :type timeline: Timeline
        """
        pass
