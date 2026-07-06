import os
import subprocess
import sys

import pytest

ALEMBIC_BIN = os.path.join(os.path.dirname(sys.executable), "alembic")


@pytest.mark.skipif(
    os.getenv("SKIP_MIGRATION_TEST") == "1" or os.getenv("TEST_DATABASE_URL") is None,
    reason="Migration test skipped by env flag or TEST_DATABASE_URL not set",
)
def test_alembic_upgrade_head():
    env = os.environ.copy()
    env["DATABASE_URL"] = os.getenv("TEST_DATABASE_URL")
    result = subprocess.run(
        [ALEMBIC_BIN, "upgrade", "head"],
        cwd=os.path.dirname(__file__) + "/..",
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Alembic upgrade failed: {result.stderr}"
