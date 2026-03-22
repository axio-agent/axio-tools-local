"""Tests for WriteFile tool handler."""

from __future__ import annotations

import os
from pathlib import Path

from axio_tools_local.write_file import WriteFile


class TestWriteFile:
    async def test_write_and_read_back(self, tmp_path: Path) -> None:
        target = tmp_path / "out.txt"
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            handler = WriteFile(file_path="out.txt", content="hello world")
            result = await handler()
            assert "11" in result  # 11 bytes
            assert target.read_text() == "hello world"
        finally:
            os.chdir(old_cwd)

    async def test_creates_subdirectories(self, tmp_path: Path) -> None:
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            handler = WriteFile(file_path="sub/dir/file.txt", content="nested")
            await handler()
            assert (tmp_path / "sub" / "dir" / "file.txt").read_text() == "nested"
        finally:
            os.chdir(old_cwd)

    async def test_repr(self) -> None:
        handler = WriteFile(file_path="f.txt", content="abc")
        assert "f.txt" in repr(handler)
        assert "3 chars" in repr(handler)
