import typing, clr, abc
from System import Array_1, IDisposable
from Microsoft.Xna.Framework.Graphics import GraphicsDevice, Texture2D, VertexPositionColorTexture
from Microsoft.Xna.Framework import Vector2, Rectangle, Color

class IFontLoader(typing.Protocol):
    @abc.abstractmethod
    def Load(self, data: Array_1[int]) -> IFontSource: ...


class IFontSource(IDisposable, typing.Protocol):
    @abc.abstractmethod
    def GetGlyphId(self, codepoint: int) -> typing.Optional[int]: ...
    @abc.abstractmethod
    def GetGlyphKernAdvance(self, previousGlyphId: int, glyphId: int, fontSize: float) -> int: ...
    @abc.abstractmethod
    def GetGlyphMetrics(self, glyphId: int, fontSize: float, advance: clr.Reference[int], x0: clr.Reference[int], y0: clr.Reference[int], x1: clr.Reference[int], y1: clr.Reference[int]) -> None: ...
    @abc.abstractmethod
    def GetMetricsForSize(self, fontSize: float, ascent: clr.Reference[int], descent: clr.Reference[int], lineHeight: clr.Reference[int]) -> None: ...
    @abc.abstractmethod
    def RasterizeGlyphBitmap(self, glyphId: int, fontSize: float, buffer: Array_1[int], startIndex: int, outWidth: int, outHeight: int, outStride: int) -> None: ...


class IFontStashRenderer(typing.Protocol):
    @property
    def GraphicsDevice(self) -> GraphicsDevice: ...
    @abc.abstractmethod
    def Draw(self, texture: Texture2D, pos: Vector2, src: typing.Optional[Rectangle], color: Color, rotation: float, scale: Vector2, depth: float) -> None: ...


class IFontStashRenderer2(typing.Protocol):
    @property
    def GraphicsDevice(self) -> GraphicsDevice: ...
    @abc.abstractmethod
    def DrawQuad(self, texture: Texture2D, topLeft: clr.Reference[VertexPositionColorTexture], topRight: clr.Reference[VertexPositionColorTexture], bottomLeft: clr.Reference[VertexPositionColorTexture], bottomRight: clr.Reference[VertexPositionColorTexture]) -> None: ...

