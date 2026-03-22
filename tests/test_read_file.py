"""Tests for ReadFile tool handler."""

from __future__ import annotations

import os
from pathlib import Path

from axio_tools_local.read_file import ReadFile


class TestReadFile:
    async def test_read_text(self, tmp_path: Path) -> None:
        (tmp_path / "hello.txt").write_text("content here")
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            handler = ReadFile(filename="hello.txt")
            result = await handler()
            assert result == "content here"
        finally:
            os.chdir(old_cwd)

    async def test_read_binary_as_hex(self, tmp_path: Path) -> None:
        (tmp_path / "bin.dat").write_bytes(b"\x80\x81\xff")
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            handler = ReadFile(filename="bin.dat", binary_as_hex=True)
            result = await handler()
            assert "8081ff" in result
        finally:
            os.chdir(old_cwd)

    async def test_file_not_found(self, tmp_path: Path) -> None:
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            handler = ReadFile(filename="nope.txt")
            try:
                await handler()
                assert False, "Should have raised"
            except FileNotFoundError:
                pass
        finally:
            os.chdir(old_cwd)

    async def test_repr(self) -> None:
        handler = ReadFile(filename="test.py")
        assert "test.py" in repr(handler)
