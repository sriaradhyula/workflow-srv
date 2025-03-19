import logging

from uvicorn.logging import ColourizedFormatter

handler = logging.StreamHandler()
colorformatter = ColourizedFormatter(
    fmt="%(levelprefix)s %(name)s %(message)s ", use_colors=True
)
handler.setFormatter(colorformatter)

CustomLoggerHandler = handler
