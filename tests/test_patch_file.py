"""Tests for PatchFile tool handler."""

from __future__ import annotations

import os
from pathlib import Path

from axio_tools_local.patch_file import PatchFile


class TestPatchFile:
    async def test_patch_lines(self, tmp_path: Path) -> None:
        target = tmp_path / "file.txt"
        target.write_text("line0\nline1\nline2\nline3\n")
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            handler = PatchFile(file_path="file.txt", from_line=1, to_line=3, content="replaced\n")
            result = await handler()
            assert "bytes written" in result
            content = target.read_text()
            assert "replaced" in content
            assert "line1" not in content
            assert "line2" not in content
        finally:
            os.chdir(old_cwd)

    async def test_file_not_found(self, tmp_path: Path) -> None:
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            handler = PatchFile(file_path="missing.txt", from_line=0, to_line=1, content="x")
            try:
                await handler()
                assert False, "Should have raised"
            except FileNotFoundError:
                pass
        finally:
            os.chdir(old_cwd)

    async def test_repr(self) -> None:
        handler = PatchFile(file_path="f.py", from_line=5, to_line=10, content="code")
        r = repr(handler)
        assert "f.py" in r
        assert "5:10" in r
