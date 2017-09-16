class ClientPackets:
    Login,  \
    SendCreateChar, \
    SendMeneNameConfirm,    \
    LatencyTick,    \
    CreateGuild,    \
    LeaveGuild, \
    SendMove,   \
    StopMove,   \
    SendFaceTarget, \
    PlayerMovePath, \
    StopTalkWithNPC,    \
    TalkWithNPC,    \
    SendMessage,    \
    RespondGuildInvite, \
    GetReport,  \
    SendReport,   \
    SolveReport,    \
    DeleteMail, \
    RespondPartyInvite, \
    SendFightReady, \
    SendAttack, \
    SendHealMenes,  \
    SendBuyItem,    \
    ThrowES,    \
    ChangeDefaultMene,  \
    SendLeaveMatch, \
    RequestMap, \
    SendMoveTarget,  \
    SendMeneNameDouble  \
    = range(29)
    
class ServerPackets:
    RequestAuth, \
    CreateCharInit, \
    SendChar,    \
    CreateMeneInit,  \
    LatencyTick,    \
    ErrorMsg,   \
    SendGuildmembers,   \
    SendJoinedGuild,    \
    SendNpcsFromMap,    \
    SendNpcMove,    \
    SendNpcDir, \
    SendRefreshName,    \
    GuildMemberPromoted,    \
    SendLeaveGuild, \
    PlayerMove, \
    PlayerMoveNext, \
    PlayerMoveStop, \
    PlayerMoveReal, \
    PlayerDirection,    \
    PlayerMovePath, \
    SendCharsFromMap,   \
    SendPlayerConnect,  \
    SendPlayerDisconnect,   \
    PlayerWhisper,  \
    PlayerGuildMsg, \
    PlayerChatMsg,  \
    SendIgnores,    \
    RemoveIgnore,   \
    SendFriends, \
    RemoveFriend,    \
    FriendLoggedIn, \
    FriendLoggedOut, \
    GuildMemberLogged,  \
    SendGuildInvite,    \
    GuildMemberKicked,  \
    PlayerTeleportLeave,    \
    PlayerTeleportSelf, \
    PlayerTeleportJoin, \
    Banned, \
    SendGetReport,  \
    SendMails,  \
    SendPartyInvite,    \
    PlayerPartyMsg, \
    SendPlayerJoinsParty,   \
    SendPlayerLeavesParty,  \
    SendMenes,  \
    StartFight, \
    SendFightTriggerToMap,  \
    SendAttack, \
    XpReceived, \
    EndMatch,   \
    HealMenes,   \
    MeneDies,    \
    SendItems,   \
    SendMoneyUpdate, \
    ThrowES, \
    ChangeFightMene, \
    InitiateMeneSelect,  \
    MoneyReceived   \
    = range(59)

class LoginClientPackets:
    SendLoginInformation,    \
    Hitler  \
    =range(2)
class LoginServerPackets:
    AskForLoginInformation,  \
    VersionOutdated,  \
    LoginWrong,  \
    PasswordOK,  \
    Banned,  \
    GameServerDown  \
    = range(6)