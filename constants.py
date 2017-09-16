#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import global_vars as g

GAME_VERSION="0.1f"
# Server information
GAME_IP = "login.sakkee.org"

# Tilesheet width
# - Number of tiles in width in tileset
TILESHEET_WIDTH = 32

# Tile size
TILESIZE = 32
#How much bigger ingame tilesize in comparison to tilesheet tilesize
TILE_SCALE=1


###############################################
# VALUES BELOW MUST MATCH THE SERVER'S VALUES #
###############################################

# general constants
GAME_NAME = "Spurdola"  # the game name
GAME_PORT = 2729      # the game port

# website
GAME_WEBSITE = "https://sakkee.org"

# account constants
NAME_LENGTH = 20

LOGINMENUSONG = 'pokemon'


GAMESTATE_LOGIN = 0
GAMESTATE_INGAME = 1
GAMESTATE_EXIT = 4
GAMESTATE_LOADING=5
GAMESTATE_CREATECHAR=2
GAMESTATE_NAMEMENE=3
GAMESTATE_FIGHTING=6
GAMESTATE_LOADING_FIGHTING=7
GAMESTATE_AUTH=8

WARNINGS= {
    "CHATSPAM":['Stop spamming you idiot :DD',g.errorColor],
    "HELP":["Type /help to see chat functions :D", g.helpColor],
    "HELPFUNCTIONS":["/help -- shows chat functions\n\n/ignore NAME -- mutes or unmutes a person in chat\n\n/friend NAME -- adds/removes a person in/from the friend list\n\n/w NAME -- sends a private message\n\n/fps -- shows FPS\n\n/g TEXT -- Sends a message to guild\n\n/reloadui -- Reloads UI, might be a cure to cancer",g.helpColor],
    "CHAR_NOT_FOUND":["%s not found!",g.errorColor],
    "IGNORED":["%s is now ignored.",g.errorColor],
    "UNIGNORED":["%s is now unignored",g.greenColor],
    "CANT_IGNORE_SELF":["%s is you! You can't ignore yourself :D",g.errorColor],
    "IGNORING":["%s is ignoring you.",g.errorColor],
    "IGNORING_NOT":["%s is not on your ignore list!",g.errorColor],
    "CANT_FRIEND_SELF":["%s is you! You can't be a friend with yourself you fugging loser :DDD",g.errorColor],
    "FRIENDED":["%s is now added to your friendlist.", g.greenColor],
    "UNFRIENDED":["%s is now removed from the friendlist.", g.errorColor],
    "FRIENDLOGGEDIN":["%s has logged in.",g.helpColor],
    "FRIENDLOGGEDOUT":["%s has logged out.",g.helpColor],
    "CANT_UNFRIEND_SELF":["%s is you! You can't unfriend yourself :D pathetic :D", g.errorColor],
    "NOT_FRIENDS":["%s isn't your friend.",g.errorColor],
    "NOT_ADMIN":["You are not an admin :(",g.errorColor],
    "WRONG_TELEPORT":['/teleport <PLAYERNAME> <TARGETPLAYER>|<MAPNAME>,<X>,<Y>',g.helpColor],
    "IS_NOW_MUTED":["%s is now muted and can only whisper.",g.errorColor],
    "WRONG_MUTE":['/mute <PLAYERNAME> <MINUTES> <REASON>',g.helpColor],
    "EMPTY_MESSAGE":["%s.",g.errorColor],
    "WRONG_UNMUTE":['/unmute <PLAYERNAME>',g.helpColor],
    "IS_NOW_UNMUTED":['%s is now unmuted.',g.greenColor],
    "UNMUTED":["%s unmuted you.",g.greenColor],
    "IS_NOW_BANNED":["%s is now banned.",g.errorColor],
    "WRONG_BAN":['/ban <PLAYERNAME> <MINUTES> <REASON>',g.helpColor],
    "WRONG_UNBAN":['/unban <PLAYERNAME>',g.helpColor],
    "IS_NOW_UNBANNED":['%s is now unbanned.',g.greenColor],
    "IS_NOT_BANNED":["%s wasn't among the banned players - didn't unban anyone.",g.errorColor],
    "NEW_REPORT":["New ticket has been opened.",g.errorColor],
    "GUILD_NAME_EXISTS":["%s exists already! You must choose a new guild name.", g.errorColor],
    "INVALID_GUILD_NAME":["%s is invalid guild name. Choose a new guild name.",g.errorColor],
    "GUILD_CREATED":["%s created.",g.greenColor],
    "LEFT_GUILD":["You have left the guild.",g.errorColor],
    "PLAYER_ALREADY_IN_GUILD":["You are already in a guild!",g.errorColor],
    'MUTED_YOU':["%s muted you for %s minutes. Reason: %s.",g.errorColor],
    'YOU_ARE_MUTED': ['You are muted. Reason: %s, seconds till unmute: %s',g.errorColor],
    "THE_PLAYER_ALREADY_IN_GUILD":["%s is already in a guild!",g.errorColor],
    'WANTS_TO_INVITE_YOU':["%s invites you to %s.", g.greenColor],
    'YOU_ARE_NOT_IN_A_GUILD':["You are not in a guild!", g.errorColor],
    'YOU_DONT_HAVE_ACCESS_TO_DO_THAT':["You don't have access to do that!", g.errorColor],
    'PLAYER_REFUSED_INVITE':["%s refused your invite!",g.errorColor],
    'GUILD_MEMBER_LOGGED_OUT':['%s has logged out.',g.greenColor],
    'GUILD_MEMBER_LOGGED_IN': ['%s has logged in.',g.greenColor],
    'CHAR_NOT_IN_SAME_GUILD': ["%s isn't in the same guild with you!", g.errorColor],
    'NOT_ACCESS': ["You don't have access to do that.", g.errorColor],
    "GUILD_MEMBER_PROMOTED": ["%s promoted %s to %s.", g.greenColor],
    "GUILD_MEMBER_DEMOTED": ["%s demoted %s to %s.", g.greenColor],
    "GUILD_NAME_TOO_SHORT": ["%s is too short name for a guild!", g.errorColor],
    "GUILD_MEMBER_KICKED": ["%s kicked %s from %s.",g.greenColor],
    "YOU_HAVE_BEEN_KICKED_FROM_GUILD":["%s kicked you from %s!", g.errorColor],
    "WILD_APPEARED":["Wild %s appeared!",g.errorColor],
    'UPDATE_AVAILABLE':["Update is available. Do you want to install?",g.errorColor],
    "INVALID_MENE_NAME":["%s doesn't seem to be a valid name for a mene. Choose a new one.",g.errorColor],
    "YOUR_MENE_NAME":["%s will be the name of the mene. Are you okay with this?",g.greenColor],
    "GUILD_INVITE_SENT":["%s has been invited to your guild.",g.greenColor],
    'CANT_PARTYINVITE_SELF':["%s is you! Can't invite yourself to a party, loser :DD",g.errorColor],
    'ALREADY_IN_PARTY':["%s is already in a party.",g.errorColor],
    'NOT_PARTYOWNER':["You are not the party leader ;__;",g.errorColor],
    'WRONG_INVITE':["/invite PLAYERNAME",g.errorColor],
    'PARTY_IS_FULL':["The party is full, couldn't join ;__;",g.errorColor],
    'WANTS_TO_INVITE_YOU_PARTY':["%s wants to invite you to his party.",g.errorColor],
    'YOU_ARE_NOT_IN_A_PARTY':["You are not in a party!",g.errorColor],
    'PARTY_INVITE_SENT':['%s has been invited to your party.',g.partyColor],
    "HAS_JOINED_PARTY":['%s has joined the party.',g.partyColor],
    "HAS_LEFT_PARTY":['%s has left the party.',g.partyColor],
    "PARTY_CREATED":["You have created a party",g.partyColor],
    "YOU_JOINED_PARTY":["You have joined a party",g.partyColor],
    "YOU_LEFT_PARTY":["You have left the party.",g.partyColor],
    'PARTY_FULL':["The party is full!",g.errorColor],
    'YOU_WERE_KICKED_FROM_PARTY':["You have been kicked from the party!",g.partyColor],
    "KICKED_FROM_PARTY":["%s has been kicked from the party.",g.partyColor],
    "ENEMY_MENE_DIED":["%s slept away! +%.2f euros",g.greenColor],
    'NEW_LEVEL':["Gz faggot :D! %s reached level %s!",g.greenColor],
    'MENES_HEALED':["Your menes have been healed!",g.greenColor],
    'YOUR_MENE_DIED':["FUGGGG :D %s slept away! ;__;",g.errorColor],
    "MENE_CAPTURED":["%s has been gabdured :DD give a name :D",g.greenColor],
    "LEAVE_MATCH":["Do you really want to be a pussy :DDDD? SHOUTENINGS :D",g.errorColor]
    
    
    
}
CHAT_SHORTMSG_TIME = 3000
CHAT_NORMALMSG_TIME = 4000
CHAT_LONGMSG_TIME = 6000

MAXCHATLOGLENGTH=10000

MAX_CHAT_INPUT = 80
# tile constants
TILE_TYPE_WALKABLE = 0
TILE_TYPE_BLOCKED  = 1
TILE_TYPE_WARP     = 2
TILE_TYPE_FIGHT     = 5
TILE_TYPE_NPCAVOID = 4


# direction constants
DIR_UP = 2
DIR_LEFT = 1
DIR_DOWN = 0
DIR_RIGHT = 3

WALKSPEED = 640 #milliseconds
# player movement
MOVING_WALKING = 1
MOVING_RUNNING = 2

# admin constants
ADMIN_MODERATOR   = 1
ADMIN_ADMIN    = 2
ADMIN_CREATOR = 3

PING_TYPE_GREEN=0
PING_TYPE_YELLOW=1
PING_TYPE_RED=2

NPC_WALKTYPE_STOPPED=0
NPC_WALKTYPE_RESTRICTED=1
NPC_WALKTYPE_FREEWALK=2

NPC_ACTIONTYPE_TALK=0
NPC_ACTIONTYPE_HEAL=1
NPC_ACTIONTYPE_SHOP=2

PLAYER_TYPE_PLAYER=0
PLAYER_TYPE_NPC=1

MAX_NPC_TALK_DISTANCE=2

HOVERING_PING=1
HOVERING_ABILITY=2
HOVERING_BAG=3
HOVERING_ITEM=4

ABILITYTYPE_ATTACK=0
ABILITYTYPE_HEAL=1

GUILD_MEMBER=0
GUILD_MODERATOR=1
GUILD_ADMIN=2

FIGHTMUSIC = 'symphonic_metal_challenge'
FIGHTWIN = 'win'
FIGHTLOSS = 'loss'

PLAYER_ONE_TURN=1
PLAYER_TWO_TURN=2

ENEMY_TEAM=0
OWN_TEAM=1

ABILITY_TYPE_ATTACK=0
ABILITY_TYPE_HEAL=1

ATTACK_RNG_MISS=0
ATTACK_RNG_NORMAL=1
ATTACK_RNG_CRIT=2

SHOWUP_NORMAL=1
SHOWUP_UNCOMMON=2
SHOWUP_RARE=3

MATCH_IN_PROGRESS=1
MATCH_PLAYER_WON=2
MATCH_NPC_WON=3
MATCH_MENE_CAUGHT=4
MATCH_PLAYER_LEFT=5
#COLOR_KEY = (255,0,255)
