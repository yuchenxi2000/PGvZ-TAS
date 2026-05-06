import clr, abc
from System.Buffers import OperationStatus
from System import ReadOnlySpan_1, Span_1

class Utf8(abc.ABC):
    @staticmethod
    def FromUtf16(source: ReadOnlySpan_1[str], destination: Span_1[int], charsRead: clr.Reference[int], bytesWritten: clr.Reference[int], replaceInvalidSequences: bool = ..., isFinalBlock: bool = ...) -> OperationStatus: ...
    @staticmethod
    def ToUtf16(source: ReadOnlySpan_1[int], destination: Span_1[str], bytesRead: clr.Reference[int], charsWritten: clr.Reference[int], replaceInvalidSequences: bool = ..., isFinalBlock: bool = ...) -> OperationStatus: ...

