"""网页速度动作和只读同步状态，均由游戏主线程调用。"""
import re
from fractions import Fraction

import System
from pgvz import (
    GetLawnApp, GetGlobalSpeedExact, GetBoardSpeedExact,
    SetGlobalSpeedExact, SetBoardSpeed, SetBoardSpeedExact,
)


class InvalidSpeed(ValueError):
    pass


class SpeedBoardChanged(RuntimeError):
    pass


def _parse_speed(value):
    text = value.strip()
    fraction = re.fullmatch(r'([0-9]+)\s*/\s*([0-9]+)', text)
    if fraction:
        return tuple(map(int, fraction.groups()))
    if re.fullmatch(r'(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)', text):
        return text
    raise ValueError('expected a decimal or a fraction')


class SpeedControl:
    def __init__(self):
        self._board_ref = None
        self._board_id = 0
        self._last_snapshot = {}

    def _current_board(self):
        app = GetLawnApp()
        board = app.mBoard if app is not None else None
        previous = self._board_ref.Target if self._board_ref is not None else None
        if not System.Object.ReferenceEquals(previous, board):
            self._board_id += 1
            self._board_ref = System.WeakReference(board) if board is not None else None
        return board

    def _read_state(self, fields):
        state = {}
        if 'global' in fields:
            try:
                is_fast, factor = GetGlobalSpeedExact()
            except ValueError:
                state['global'] = None
            else:
                numerator, denominator = (factor, 1) if is_fast else (1, factor)
                state['global'] = {'numerator': numerator, 'denominator': denominator}
        if 'board' in fields:
            board = self._current_board()
            state['board'] = None
            if board is not None:
                numerator, denominator = GetBoardSpeedExact(board)
                state['board'] = {
                    'id': self._board_id, 'numerator': numerator, 'denominator': denominator,
                }
        return state

    def to_dict(self, fields=None):
        state = self._read_state(('global', 'board') if fields is None else fields)
        self._last_snapshot.update(state)
        return state

    def changed_fields(self):
        state = self._read_state(('global', 'board'))
        return tuple(field for field, value in state.items() if value != self._last_snapshot.get(field))

    def set_global(self, value):
        try:
            parsed = _parse_speed(value)
            ratio = Fraction(*parsed) if isinstance(parsed, tuple) else Fraction(parsed)
            if ratio.denominator == 1:
                SetGlobalSpeedExact(True, ratio.numerator)
            elif ratio.numerator == 1:
                SetGlobalSpeedExact(False, ratio.denominator)
            else:
                raise ValueError('global speed must be an integer or its reciprocal')
        except (TypeError, ValueError, ZeroDivisionError, OverflowError) as error:
            raise InvalidSpeed(str(error))

    def set_board(self, board_id, value):
        board = self._current_board()
        if board is None or board_id != self._board_id:
            raise SpeedBoardChanged('the current board has changed')
        try:
            parsed = _parse_speed(value)
            if isinstance(parsed, tuple):
                SetBoardSpeedExact(parsed[0], parsed[1], board)
            else:
                SetBoardSpeed(float(parsed), board=board)
        except (TypeError, ValueError, OverflowError) as error:
            raise InvalidSpeed(str(error))


speed_control = SpeedControl()
