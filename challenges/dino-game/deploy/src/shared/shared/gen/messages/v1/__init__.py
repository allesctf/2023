# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: messages/v1/entity.proto, messages/v1/messages.proto, messages/v1/tile.proto
# plugin: python-betterproto
# This file has been @generated

from dataclasses import dataclass
from datetime import datetime
from typing import List

import betterproto


class Direction(betterproto.Enum):
    DIRECTION_UNSPECIFIED = 0
    DIRECTION_NORTH = 1
    DIRECTION_EAST = 2
    DIRECTION_SOUTH = 3
    DIRECTION_WEST = 4


class Activity(betterproto.Enum):
    ACTIVITY_UNSPECIFIED = 0
    ACTIVITY_IDLE = 1
    ACTIVITY_WALKING = 2
    ACTIVITY_ATTACKING = 3
    ACTIVITY_DEATH = 4


class ObjectType(betterproto.Enum):
    OBJECT_TYPE_UNSPECIFIED = 0
    OBJECT_TYPE_NPC = 1
    OBJECT_TYPE_ENEMY = 2
    OBJECT_TYPE_AREA = 3
    OBJECT_TYPE_PICKUPABLE = 4


class InteractStatus(betterproto.Enum):
    INTERACT_STATUS_UNSPECIFIED = 0
    INTERACT_STATUS_START = 1
    INTERACT_STATUS_UPDATE = 2
    INTERACT_STATUS_STOP = 3


class InteractType(betterproto.Enum):
    INTERACT_TYPE_UNSPECIFIED = 0
    INTERACT_TYPE_TEXT = 1
    INTERACT_TYPE_SHOP = 2
    INTERACT_TYPE_DIG = 3
    INTERACT_TYPE_RUNNER = 4
    INTERACT_TYPE_CUT_OUT = 5
    INTERACT_TYPE_LICENSE = 6


class ShopInteractType(betterproto.Enum):
    SHOP_INTERACT_TYPE_UNSPECIFIED = 0
    SHOP_INTERACT_TYPE_BUY = 1
    SHOP_INTERACT_TYPE_SELL = 2
    SHOP_INTERACT_TYPE_TRADE = 3


class RunnerAction(betterproto.Enum):
    RUNNER_ACTION_UNSPECIFIED = 0
    RUNNER_ACTION_JUMP = 1
    RUNNER_ACTION_MAYBE_ADD_OBSTACLE = 2
    RUNNER_ACTION_DIE = 3


class SessionType(betterproto.Enum):
    SESSION_TYPE_UNSPECIFIED = 0
    SESSION_TYPE_NORMAL = 1
    SESSION_TYPE_FREE_CAM = 2


class ErrorType(betterproto.Enum):
    ERROR_TYPE_UNSPECIFIED = 0
    ERROR_TYPE_UNAUTHORIZED = 1
    ERROR_TYPE_INVALID_CHUNK = 2
    ERROR_TYPE_INVALID_OBJECT = 3
    ERROR_TYPE_TIMEOUT = 4
    ERROR_TYPE_ALREADY_LOGGED_IN = 5


@dataclass(eq=False, repr=False)
class Point(betterproto.Message):
    x: float = betterproto.double_field(1)
    y: float = betterproto.double_field(2)


@dataclass(eq=False, repr=False)
class Polygon(betterproto.Message):
    points: List["Point"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class TileCollision(betterproto.Message):
    polygons: List["Polygon"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class AnimationStep(betterproto.Message):
    id: int = betterproto.int32_field(1)
    duration: int = betterproto.int32_field(2)


@dataclass(eq=False, repr=False)
class Animation(betterproto.Message):
    id: int = betterproto.int32_field(1)
    animation_setps: List["AnimationStep"] = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class Tileset(betterproto.Message):
    tileset: bytes = betterproto.bytes_field(1)
    width: int = betterproto.int32_field(2)
    height: int = betterproto.int32_field(3)
    animations: List["Animation"] = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class Object(betterproto.Message):
    uuid: str = betterproto.string_field(1)
    coords: "Coords" = betterproto.message_field(2)
    type: "ObjectType" = betterproto.enum_field(3)
    remove: bool = betterproto.bool_field(4)
    enemy_info: "EnemyInfo" = betterproto.message_field(5)
    area: "Polygon" = betterproto.message_field(6)
    pickupable: "Item" = betterproto.message_field(7)


@dataclass(eq=False, repr=False)
class EnemyInfo(betterproto.Message):
    health: int = betterproto.int32_field(1)
    health_max: int = betterproto.int32_field(2)
    name: str = betterproto.string_field(3)
    last_attack: float = betterproto.double_field(4)


@dataclass(eq=False, repr=False)
class Objects(betterproto.Message):
    objects: List["Object"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class ObjectAssetRequest(betterproto.Message):
    uuid: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class EntityAsset(betterproto.Message):
    id: int = betterproto.int32_field(1)
    direction: "Direction" = betterproto.enum_field(2)
    activity: "Activity" = betterproto.enum_field(3)


@dataclass(eq=False, repr=False)
class EntityAssets(betterproto.Message):
    height: int = betterproto.int32_field(1)
    width: int = betterproto.int32_field(2)
    tileset: "Tileset" = betterproto.message_field(3)
    entity_assets: List["EntityAsset"] = betterproto.message_field(4)
    collisions: List["TileCollision"] = betterproto.message_field(5)


@dataclass(eq=False, repr=False)
class ObjectAsset(betterproto.Message):
    object_uuid: str = betterproto.string_field(1)
    assets: "EntityAssets" = betterproto.message_field(2)
    name: str = betterproto.string_field(3)
    type: "ObjectType" = betterproto.enum_field(4)
    interactable: bool = betterproto.bool_field(5)
    interact_distance: float = betterproto.double_field(6)


@dataclass(eq=False, repr=False)
class Interact(betterproto.Message):
    uuid: str = betterproto.string_field(1)
    text: str = betterproto.string_field(2)
    status: "InteractStatus" = betterproto.enum_field(3)
    type: "InteractType" = betterproto.enum_field(4)
    shop: List["ShopInteract"] = betterproto.message_field(5)
    progress: float = betterproto.double_field(6)
    runner: "Runner" = betterproto.message_field(7)


@dataclass(eq=False, repr=False)
class ShopInteract(betterproto.Message):
    item: "Item" = betterproto.message_field(1)
    cost: int = betterproto.int32_field(2)
    type: "ShopInteractType" = betterproto.enum_field(3)
    trade_in: "Item" = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class Item(betterproto.Message):
    name: str = betterproto.string_field(1)
    description: str = betterproto.string_field(2)
    icon: int = betterproto.int32_field(3)
    quantity: int = betterproto.int32_field(4)


@dataclass(eq=False, repr=False)
class RunnerEvent(betterproto.Message):
    time: float = betterproto.double_field(1)
    action: "RunnerAction" = betterproto.enum_field(2)


@dataclass(eq=False, repr=False)
class Runner(betterproto.Message):
    events: List["RunnerEvent"] = betterproto.message_field(1)
    dts: List[float] = betterproto.double_field(2)


@dataclass(eq=False, repr=False)
class Coords(betterproto.Message):
    x: float = betterproto.double_field(1)
    y: float = betterproto.double_field(2)
    rotation: float = betterproto.double_field(3)


@dataclass(eq=False, repr=False)
class User(betterproto.Message):
    uuid: str = betterproto.string_field(1)
    username: str = betterproto.string_field(2)
    coords: "Coords" = betterproto.message_field(3)
    money: int = betterproto.int32_field(4)
    inventory: List["Item"] = betterproto.message_field(5)
    health: int = betterproto.int32_field(6)
    last_death: float = betterproto.float_field(7)


@dataclass(eq=False, repr=False)
class Users(betterproto.Message):
    users: List["User"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class Login(betterproto.Message):
    username: str = betterproto.string_field(1)
    password: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class LoggedIn(betterproto.Message):
    success: bool = betterproto.bool_field(1)
    self: "User" = betterproto.message_field(2)
    assets: "EntityAssets" = betterproto.message_field(3)
    interact_distance: float = betterproto.double_field(4)
    type: "SessionType" = betterproto.enum_field(5)
    error: "ErrorType" = betterproto.enum_field(6)


@dataclass(eq=False, repr=False)
class Ping(betterproto.Message):
    time: datetime = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class MapChunk(betterproto.Message):
    x: int = betterproto.int32_field(1)
    y: int = betterproto.int32_field(2)
    height: int = betterproto.int32_field(3)
    width: int = betterproto.int32_field(4)
    tiles: List[int] = betterproto.int32_field(5)
    tileset: "Tileset" = betterproto.message_field(6)
    collisions: List["TileCollision"] = betterproto.message_field(7)


@dataclass(eq=False, repr=False)
class MapChunkRequest(betterproto.Message):
    x: int = betterproto.int32_field(1)
    y: int = betterproto.int32_field(2)


@dataclass(eq=False, repr=False)
class Error(betterproto.Message):
    type: "ErrorType" = betterproto.enum_field(1)
    message: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class Logout(betterproto.Message):
    user: "User" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class GiveDamage(betterproto.Message):
    """Message related to fighting"""

    damage: int = betterproto.int32_field(1)


@dataclass(eq=False, repr=False)
class AcknowledgeDamage(betterproto.Message):
    damage: int = betterproto.int32_field(1)


@dataclass(eq=False, repr=False)
class AttackEnemy(betterproto.Message):
    time: datetime = betterproto.message_field(1)
    uuid: str = betterproto.string_field(2)
    damage: int = betterproto.int32_field(3)


@dataclass(eq=False, repr=False)
class ClientMessage(betterproto.Message):
    ping: "Ping" = betterproto.message_field(1, group="message")
    login: "Login" = betterproto.message_field(2, group="message")
    coords: "Coords" = betterproto.message_field(3, group="message")
    chunk_request: "MapChunkRequest" = betterproto.message_field(4, group="message")
    object_asset_request: "ObjectAssetRequest" = betterproto.message_field(
        5, group="message"
    )
    interact: "Interact" = betterproto.message_field(6, group="message")
    acknowledge_damage: "AcknowledgeDamage" = betterproto.message_field(
        7, group="message"
    )
    attack_enemy: "AttackEnemy" = betterproto.message_field(8, group="message")
    logout: "Logout" = betterproto.message_field(9, group="message")
    uuid: str = betterproto.string_field(100)


@dataclass(eq=False, repr=False)
class MapChunkResponse(betterproto.Message):
    chunks: List["MapChunk"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class ServerMessage(betterproto.Message):
    ping: "Ping" = betterproto.message_field(1, group="message")
    logged_in: "LoggedIn" = betterproto.message_field(2, group="message")
    users: "Users" = betterproto.message_field(3, group="message")
    chunk: "MapChunkResponse" = betterproto.message_field(4, group="message")
    error: "Error" = betterproto.message_field(5, group="message")
    logout: "Logout" = betterproto.message_field(6, group="message")
    objects: "Objects" = betterproto.message_field(7, group="message")
    object_asset: "ObjectAsset" = betterproto.message_field(8, group="message")
    interact: "Interact" = betterproto.message_field(9, group="message")
    give_damage: "GiveDamage" = betterproto.message_field(10, group="message")
    uuid: str = betterproto.string_field(100)
