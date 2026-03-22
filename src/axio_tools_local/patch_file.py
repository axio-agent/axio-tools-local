import asyncio
import os
from pathlib import Path

from axio.tool import ToolHandler


class PatchFile(ToolHandler):
    """Replace a range of lines in an existing file. Lines are 0-indexed:
    from_line is inclusive, to_line is exclusive. The content string replaces
    lines[from_line:to_line]. Always read the file first to get correct
    line numbers. Use this for surgical edits instead of rewriting the
    whole file with write_file."""

    file_path: str
    mode: int = 0o644
    from_line: int
    to_line: int
    content: str

    def __repr__(self) -> str:
        return (
            f"PatchFile(file_path={self.file_path!r},"
            f" lines={self.from_line}:{self.to_line}, content=<{len(self.content)} chars>)"
        )

    def _blocking(self) -> str:
        path = Path(os.getcwd()) / self.file_path
        if not path.is_file():
            raise FileNotFoundError(f"{self.file_path} is not a valid file")

        # read all lines
        with path.open("r") as f:
            lines = f.readlines()

        # content lines
        content = self.content.splitlines()

        # patch lines
        new_lines = lines[: self.from_line] + content + lines[self.to_line :]
        with path.open("w") as f:
            f.writelines(new_lines)
            return f"{f.tell()} bytes written to {self.file_path}"

    async def __call__(self) -> str:
        return await asyncio.to_thread(self._blocking)
