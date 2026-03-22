"""Tests for ListFiles tool handler."""

from __future__ import annotations

import os
from pathlib import Path

from axio_tools_local.list_files import ListFiles


class TestListFiles:
    async def test_list_directory(self, tmp_path: Path) -> None:
        (tmp_path / "a.txt").write_text("a")
        (tmp_path / "b.txt").write_text("b")
        (tmp_path / "subdir").mkdir()
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            handler = ListFiles(directory=".")
            result = await handler()
            assert "a.txt" in result
            assert "b.txt" in result
            assert "subdir/" in result
        finally:
            os.chdir(old_cwd)

    async def test_empty_directory(self, tmp_path: Path) -> None:
        empty = tmp_path / "empty"
        empty.mkdir()
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            handler = ListFiles(directory="empty")
            result = await handler()
            assert result == "(empty directory)"
        finally:
            os.chdir(old_cwd)

    async def test_default_directory(self, tmp_path: Path) -> None:
        (tmp_path / "file.txt").write_text("x")
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            handler = ListFiles()
            assert handler.directory == "."
            result = await handler()
            assert "file.txt" in result
        finally:
            os.chdir(old_cwd)

    async def test_not_a_directory(self, tmp_path: Path) -> None:
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            handler = ListFiles(directory="nope")
            try:
                await handler()
                assert False, "Should have raised"
            except FileNotFoundError:
                pass
        finally:
            os.chdir(old_cwd)
