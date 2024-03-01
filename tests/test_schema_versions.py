from datasette.app import Datasette
import httpx
import pytest
import sqlite_utils


@pytest.fixture
def datasette_and_dbs(tmpdir):
    path1 = str(tmpdir / "data1.db")
    path2 = str(tmpdir / "data2.db")
    db1 = sqlite_utils.Database(path1)
    db1["foo"].insert({"bar": 1})
    db2 = sqlite_utils.Database(path2)
    db2["foo"].insert({"bar": 1})
    return Datasette([path1, path2]), db1, db2


@pytest.mark.asyncio
async def test_schema_versions_json(datasette_and_dbs):
    datasette, db1, db2 = datasette_and_dbs
    response = await datasette.client.get("/-/schema-versions.json")
    assert 200 == response.status_code
    assert response.json() == {"data1": 1, "data2": 1, "_internal": 0}
    # Inserting records should change nothing
    db1["foo"].insert({"bar": 1})
    db2["foo"].insert({"bar": 1})
    response = await datasette.client.get("/-/schema-versions.json")
    assert response.json() == {"data1": 1, "data2": 1, "_internal": 0}
    # But modifying the schema should cause a change
    db1["baz"].insert({"baz": 1})
    response = await datasette.client.get("/-/schema-versions.json")
    assert response.json() == {"data1": 2, "data2": 1, "_internal": 0}


@pytest.mark.asyncio
async def test_schema_versions(datasette_and_dbs):
    datasette = datasette_and_dbs[0]
    response = await datasette.client.get("/-/schema-versions")
    assert response.status_code == 200
    assert "<h1>schema-versions.json</h1>" in response.text
    assert "<pre>{" in response.text
