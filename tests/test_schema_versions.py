from datasette.app import Datasette
import httpx
import pytest
import sqlite_utils


@pytest.mark.asyncio
async def test_plugin_is_installed():
    app = Datasette([], memory=True).app()
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get("http://localhost/-/plugins.json")
        assert 200 == response.status_code
        installed_plugins = {p["name"] for p in response.json()}
        assert "datasette-schema-versions" in installed_plugins


@pytest.mark.asyncio
async def test_schema_versions(tmpdir):
    path1 = str(tmpdir / "data1.db")
    path2 = str(tmpdir / "data2.db")
    db1 = sqlite_utils.Database(path1)
    db1["foo"].insert({"bar": 1})
    db2 = sqlite_utils.Database(path2)
    db2["foo"].insert({"bar": 1})
    app = Datasette([path1, path2]).app()
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get("http://localhost/-/schema-versions")
        assert 200 == response.status_code
        assert response.json() == {"data1": 1, "data2": 1}
        # Inserting records should change nothing
        db1["foo"].insert({"bar": 1})
        db2["foo"].insert({"bar": 1})
        response = await client.get("http://localhost/-/schema-versions")
        assert response.json() == {"data1": 1, "data2": 1}
        # But modifying the schema should cause a change
        db1["baz"].insert({"baz": 1})
        response = await client.get("http://localhost/-/schema-versions")
        assert response.json() == {"data1": 2, "data2": 1}
