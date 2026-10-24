from __future__ import annotations

import subprocess
import sys
import textwrap


def test_app_can_be_created_without_pydantic() -> None:
    script = textwrap.dedent(
        """
        import sys

        sys.modules["pydantic"] = None  # makes `import pydantic` raise ImportError

        from litestar import Litestar, get

        @get("/")
        async def index() -> str:
            return "ok"

        app = Litestar([index])
        assert not any(type(p).__module__.startswith("litestar.plugins.pydantic") for p in app.plugins._plugins)
        """
    )
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
