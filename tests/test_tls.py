import ssl


def test_tls_context_requires_tls_12_or_newer():
    context = ssl.create_default_context()
    context.minimum_version = ssl.TLSVersion.TLSv1_2

    assert context.minimum_version == ssl.TLSVersion.TLSv1_2