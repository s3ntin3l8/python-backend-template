import pytest
from cryptography.fernet import Fernet

from app.core.encryption import DecryptionError, EncryptionService


def test_roundtrip_with_key():
    svc = EncryptionService(key=Fernet.generate_key().decode())
    assert svc.is_enabled
    token = svc.encrypt_string("hunter2")
    assert token != "hunter2"
    assert svc.decrypt_string(token) == "hunter2"


def test_json_roundtrip_with_key():
    svc = EncryptionService(key=Fernet.generate_key().decode())
    data = {"a": 1, "b": ["x", "y"]}
    assert svc.decrypt_json(svc.encrypt_json(data)) == data


def test_passthrough_when_disabled():
    svc = EncryptionService(key="")
    assert not svc.is_enabled
    assert svc.encrypt_string("plain") == "plain"
    assert svc.decrypt_string("plain") == "plain"


def test_legacy_plaintext_is_returned_unchanged():
    # A value without the Fernet prefix is treated as legacy plaintext, not a failure.
    svc = EncryptionService(key=Fernet.generate_key().decode())
    assert svc.decrypt_string("legacy-plaintext") == "legacy-plaintext"


def test_fernet_prefixed_garbage_raises():
    svc = EncryptionService(key=Fernet.generate_key().decode())
    with pytest.raises(DecryptionError):
        svc.decrypt_string("gAAAAA-not-a-real-token")
