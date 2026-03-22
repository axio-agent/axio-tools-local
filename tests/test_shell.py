"""Tests for Shell tool handler."""

from __future__ import annotations

from pathlib import Path

from axio_tools_local.shell import Shell


class TestShell:
    async def test_echo(self) -> None:
        handler = Shell(command="echo hello", timeout=5)
        result = await handler()
        assert "hello" in result

    async def test_stderr(self) -> None:
        handler = Shell(command="echo err >&2", timeout=5)
        result = await handler()
        assert "err" in result

    async def test_nonzero_exit(self) -> None:
        handler = Shell(command="exit 42", timeout=5)
        result = await handler()
        assert "exit code: 42" in result

    async def test_cwd(self, tmp_path: Path) -> None:
        handler = Shell(command="pwd", timeout=5, cwd=str(tmp_path))
        result = await handler()
        assert str(tmp_path) in result

    async def test_stdin_devnull(self) -> None:
        """stdin must be /dev/null so subprocesses can't steal TUI key events."""
        handler = Shell(command="cat", timeout=2)
        result = await handler()
        # cat with no args + /dev/null stdin → immediate EOF → "(no output)"
        assert result == "(no output)"

    async def test_stdin_passthrough(self) -> None:
        handler = Shell(command="cat", timeout=5, stdin="hello from stdin")
        result = await handler()
        assert "hello from stdin" in result

    async def test_repr(self) -> None:
        handler = Shell(command="echo hi")
        assert "echo hi" in repr(handler)
