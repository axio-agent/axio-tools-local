import asyncio
import os

from axio.tool import ToolHandler


class ReadFile(ToolHandler):
    """Read file contents. Returns text for text files, hex for binaries.
    Use start_line/end_line to read a specific range of lines (0-indexed).
    Large files are truncated to max_chars. Always read the file before
    editing it with write_file or patch_file."""

    filename: str
    max_chars: int = 32768
    binary_as_hex: bool = True
    start_line: int | None = None
    end_line: int | None = None

    def __repr__(self) -> str:
        return f"ReadFile(filename={self.filename!r})"

    def _blocking(self) -> str:
        path = os.path.join(os.getcwd(), self.filename)
        if self.start_line is None and self.end_line is None:
            with open(path, "rb") as f:
                result = f.read(self.max_chars)
            try:
                return result.decode()
            except UnicodeDecodeError:
                if self.binary_as_hex:
                    return "Encoded binary data HEX: " + result.hex()
                raise
        with open(path) as f:
            lines = f.readlines()[self.start_line : self.end_line]
            content = "".join(lines)
            if len(content) > self.max_chars:
                return content[: self.max_chars] + "\n...[truncated]"
            return content.strip()

    async def __call__(self) -> str:
        return await asyncio.to_thread(self._blocking)
