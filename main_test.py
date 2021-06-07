import main


def test_home():
    main.app.testing = True
    client = main.app.test_client()

    r = client.get("/")
    assert r.status_code == 200
    assert "Derpysearch" in r.data.decode("utf-8")
