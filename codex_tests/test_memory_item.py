import sys
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "autogpts" / "autogpt"))

from autogpt.memory.vector.memory_item import MemoryItem


class DummyConfig:
    pass


def test_from_code_file_passes_config(mocker: MockerFixture):
    captured = {}
    config = DummyConfig()

    def fake_from_text(content, source_type, cfg, metadata):
        captured['content'] = content
        captured['source_type'] = source_type
        captured['cfg'] = cfg
        captured['metadata'] = metadata
        return "result"

    mocker.patch.object(MemoryItem, "from_text", side_effect=fake_from_text)

    result = MemoryItem.from_code_file("code", "path/to/file.py", config)

    assert result == "result"
    assert captured['source_type'] == "code_file"
    assert captured['cfg'] is config
    assert captured['metadata'] == {"location": "path/to/file.py"}
