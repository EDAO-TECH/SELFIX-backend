import pytest
import os
from pyfakefs.fake_filesystem_unittest import Patcher
from selfix.config import config
from selfix.engine.book_of_forgiveness.forgiveness_engine import ForgivenessEngine


@pytest.fixture
def engine_with_fakefs():
    with Patcher() as patcher:
        # Setup fake filesystem structure
        fake_vault = "/fake/vault"
        fake_code_dir = "/fake/code"

        patcher.fs.create_dir(fake_vault)
        patcher.fs.create_dir(fake_code_dir)

        # Override the sealed directory used by the engine
        config.SEALED_DIR = os.path.join(fake_vault)

        engine = ForgivenessEngine()
        yield engine


def test_seal_and_verify(engine_with_fakefs):
    engine = engine_with_fakefs
    test_file = "/fake/code/file.py"

    # Create a fake file to seal
    with open(test_file, "w") as f:
        f.write("print('hello')")

    # Seal it
    result = engine.seal(
        filepath=test_file,
        forgiven_by="tester",
        reason="unit test",
        alias="unit_test_script"
    )

    assert result["original_path"] == test_file
    assert result["hash"]
    assert result["executable_valid"] is True

    # Should pass verification
    assert engine.verify(test_file) is True

    # Tamper with file
    with open(test_file, "w") as f:
        f.write("tampered")

    assert engine.verify(test_file) is False


def test_restore_file(engine_with_fakefs):
    engine = engine_with_fakefs
    file_path = "/fake/code/app.py"
    sealed_path = os.path.join(config.SEALED_DIR, "app.py")

    # Create a real + sealed version
    with open(file_path, "w") as f:
        f.write("old version")

    with open(sealed_path, "w") as f:
        f.write("sealed version")

    # Restore should overwrite the file with the sealed version
    restored = engine.restore(file_path)
    assert restored is True

    with open(file_path, "r") as f:
        assert f.read() == "sealed version"


def test_missing_file_raises(engine_with_fakefs):
    engine = engine_with_fakefs

    # Should raise FileNotFoundError if file doesn't exist
    with pytest.raises(FileNotFoundError):
        engine.seal(
            filepath="/fake/missing.py",
            forgiven_by="tester",
            reason="should fail"
        )
