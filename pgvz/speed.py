"""游戏全局速度与 Board 关卡内速度的公开控制 API。"""
import math

import Lawn
import Sexy

from .util import GetBoard


MIN_GAME_SPEED = 0.01
MAX_GAME_SPEED = 100.0
DEFAULT_BOARD_SPEED_ERROR = 1e-6

_INT32_MAX = 2147483647
_MAX_CONTINUED_FRACTION_ITERATIONS = 64


def _finite_number(value, name):
    if isinstance(value, bool):
        raise TypeError('{} must be a number, not bool'.format(name))
    if isinstance(value, (str, bytes)):
        raise TypeError('{} must be a number'.format(name))
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError):
        raise TypeError('{} must be a finite number'.format(name))
    if math.isnan(result) or math.isinf(result):
        raise ValueError('{} must be a finite number'.format(name))
    return result


def _validate_speed(speed):
    value = _finite_number(speed, 'speed')
    if value < MIN_GAME_SPEED or value > MAX_GAME_SPEED:
        raise ValueError(
            'speed must be between {} and {}, got {}'.format(
                MIN_GAME_SPEED,
                MAX_GAME_SPEED,
                value,
            )
        )
    return value


def _positive_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError('{} must be an int'.format(name))
    if value <= 0:
        raise ValueError('{} must be greater than 0'.format(name))
    return value


def _resolve_board(board):
    result = GetBoard() if board is None else board
    if result is None:
        raise RuntimeError('Board speed is only available while a Board exists')
    return result


def GetGlobalSpeedExact() -> 'tuple[bool, int]':
    """返回游戏当前实际采用的全局快慢模式和整数因子。"""
    raw_factor = int(Sexy.GlobalStaticVars.gFastSlowMoNum)
    if raw_factor < 0:
        raise ValueError('gFastSlowMoNum cannot represent a valid speed')
    # LawnApp.UpdateFrames 先判断慢速，因此两个开关同时为 True 时慢速优先。
    if Sexy.GlobalStaticVars.gSlowMo:
        return False, raw_factor if raw_factor != 0 else 4
    if Sexy.GlobalStaticVars.gFastMo:
        return True, raw_factor if raw_factor != 0 else 20
    return True, 1


def GetGlobalSpeed() -> float:
    """以浮点数返回当前实际采用的全局速度。"""
    is_fast, factor = GetGlobalSpeedExact()
    return float(factor) if is_fast else 1.0 / float(factor)


def SetGlobalSpeedExact(is_fast: bool, factor: int) -> 'tuple[bool, int]':
    """用整数倍或整数倒数倍精确设置全局速度。"""
    if not isinstance(is_fast, bool):
        raise TypeError('is_fast must be a bool')
    factor = _positive_int(factor, 'factor')
    actual_speed = float(factor) if is_fast else 1.0 / float(factor)
    _validate_speed(actual_speed)

    # 先关闭两种模式，避免写入过程中短暂同时启用快慢速。
    Sexy.GlobalStaticVars.gFastMo = False
    Sexy.GlobalStaticVars.gSlowMo = False
    Sexy.GlobalStaticVars.gFastSlowMoNum = factor
    Sexy.GlobalStaticVars.gSlowMoCounter = 0
    Sexy.GlobalStaticVars.gFastMo = is_fast
    Sexy.GlobalStaticVars.gSlowMo = not is_fast
    return is_fast, factor


def SetGlobalSpeed(speed: float) -> 'tuple[bool, int]':
    """按旧修改器算法把浮点速度转换为整数倍或整数倒数倍。"""
    value = _validate_speed(speed)
    is_fast = value >= 1.0
    factor = round(value) if is_fast else round(1.0 / value)
    return SetGlobalSpeedExact(is_fast, int(factor))


def GetBoardSpeedExact(
    board: 'Lawn.Board | None' = None,
) -> 'tuple[int, int]':
    """返回 Board 当前保存的原始速度分子和分母。"""
    target = _resolve_board(board)
    return (
        int(target.mAccelerationNumerator),
        int(target.mAccelerationDenominator),
    )


def GetBoardSpeed(board: 'Lawn.Board | None' = None) -> float:
    """以浮点数返回 Board 当前保存的速度比例。"""
    numerator, denominator = GetBoardSpeedExact(board)
    if denominator == 0:
        raise ValueError('mAccelerationDenominator must not be 0')
    return float(numerator) / float(denominator)


def SetBoardSpeedExact(
    numerator: int,
    denominator: int,
    board: 'Lawn.Board | None' = None,
) -> 'tuple[int, int]':
    """直接设置 Board 分数速度，不约分。"""
    numerator = _positive_int(numerator, 'numerator')
    denominator = _positive_int(denominator, 'denominator')
    if numerator * denominator > _INT32_MAX:
        raise OverflowError(
            'numerator * denominator exceeds the safe C# int range'
        )
    _validate_speed(float(numerator) / float(denominator))
    target = _resolve_board(board)

    # 让整个写入过程始终保持合法分母，并在启用新分母前重置相位。
    target.mAccelerationDenominator = 1
    target.mAccelerationNumerator = numerator
    target.mAccelerationFrameIndex = 0
    target.mAccelerationDenominator = denominator
    return numerator, denominator


def _continued_fraction_ratio(speed, max_error):
    value = speed
    p_prev2, p_prev1 = 0, 1
    q_prev2, q_prev1 = 1, 0

    for _ in range(_MAX_CONTINUED_FRACTION_ITERATIONS):
        coefficient = int(math.floor(value))
        numerator = coefficient * p_prev1 + p_prev2
        denominator = coefficient * q_prev1 + q_prev2

        if numerator > 0:
            if numerator * denominator > _INT32_MAX:
                raise OverflowError(
                    'continued-fraction result exceeds the safe C# int range '
                    'before reaching the requested error'
                )
            actual_speed = float(numerator) / float(denominator)
            if (
                MIN_GAME_SPEED <= actual_speed <= MAX_GAME_SPEED
                and abs(actual_speed - speed) < max_error
            ):
                return numerator, denominator

        fractional_part = value - coefficient
        if fractional_part == 0.0:
            break

        p_prev2, p_prev1 = p_prev1, numerator
        q_prev2, q_prev1 = q_prev1, denominator
        value = 1.0 / fractional_part
        if math.isnan(value) or math.isinf(value):
            break

    raise OverflowError(
        'cannot represent speed within the requested error and safe C# int range'
    )


def SetBoardSpeed(
    speed: float,
    max_error: float = DEFAULT_BOARD_SPEED_ERROR,
    board: 'Lawn.Board | None' = None,
) -> 'tuple[int, int]':
    """用连分数将浮点速度转换为 Board 分子和分母。"""
    value = _validate_speed(speed)
    error = _finite_number(max_error, 'max_error')
    if error <= 0.0:
        raise ValueError('max_error must be greater than 0')
    numerator, denominator = _continued_fraction_ratio(value, error)
    return SetBoardSpeedExact(numerator, denominator, board)


__all__ = [
    'MIN_GAME_SPEED',
    'MAX_GAME_SPEED',
    'DEFAULT_BOARD_SPEED_ERROR',
    'GetGlobalSpeedExact',
    'GetGlobalSpeed',
    'SetGlobalSpeedExact',
    'SetGlobalSpeed',
    'GetBoardSpeedExact',
    'GetBoardSpeed',
    'SetBoardSpeedExact',
    'SetBoardSpeed',
]
