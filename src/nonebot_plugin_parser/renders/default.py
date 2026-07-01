"""渲染器模块 - 负责将解析结果渲染为消息"""

from typing_extensions import override

from .base import UniHelper, UniMessage, BaseRenderer
from ..helper import Text, Segment


class DefaultRenderer(BaseRenderer):
    """统一的渲染器，将解析结果转换为消息"""

    @override
    async def render_messages(self):
        texts = [
            self.result.header,
            self.result.text,
            self.result.extra_info,
        ]

        if self.append_url:
            texts.extend((self.result.display_url, self.result.repost_display_url))

        texts = [text for text in texts if text]
        texts[:-1] = [text + "\n" for text in texts[:-1]]
        segs: list[Segment] = [Text(text) for text in texts]

        if self.result.video and (cover := self.result.video.cover) and (cover_path := await cover.safe_get()):
            segs.insert(1, UniHelper.img_seg(cover_path))

        # Disable merged forwards for long text.
        yield UniMessage(segs)

        async for message in self.render_contents():
            yield message
