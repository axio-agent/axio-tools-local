"""Tests for RunPython tool handler."""

from __future__ import annotations

from axio_tools_local.run_python import RunPython


class TestRunPython:
    async def test_simple_print(self) -> None:
        handler = RunPython(code="print('hello')", timeout=5)
        result = await handler()
        assert "hello" in result

    async def test_error(self) -> None:
        handler = RunPython(code="raise ValueError('boom')", timeout=5)
        result = await handler()
        assert "ValueError" in result
        assert "exit code:" in result

    async def test_stdin_devnull(self) -> None:
        """stdin must be /dev/null so subprocesses can't steal TUI key events."""
        handler = RunPython(code="import sys; data = sys.stdin.read(); print(repr(data))", timeout=2)
        result = await handler()
        # stdin is /dev/null → immediate EOF → empty string
        assert "''" in result

    async def test_stdin_passthrough(self) -> None:
        handler = RunPython(
            code="import sys; print(sys.stdin.read())",
            timeout=5,
            stdin="hello from stdin",
        )
        result = await handler()
        assert "hello from stdin" in result

    async def test_repr(self) -> None:
        handler = RunPython(code="x = 1")
        assert "x = 1" in repr(handler)
