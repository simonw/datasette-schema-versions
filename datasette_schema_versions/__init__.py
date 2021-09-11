from datasette import hookimpl
from datasette.utils.asgi import Response
import json


async def schema_versions(datasette, request):
    return Response.html(
        await datasette.render_template(
            "show_json.html",
            {
                "filename": "schema-versions.json",
                "data_json": json.dumps(await _schema_versions(datasette), indent=4),
            },
            request=request,
        )
    )


async def schema_versions_json(datasette):
    return Response.json(await _schema_versions(datasette))


async def _schema_versions(datasette):
    schema_versions = {}
    for name, database in datasette.databases.items():
        if name != "_internal":
            schema_versions[name] = (
                await database.execute("PRAGMA schema_version")
            ).first()[0]
    return schema_versions


@hookimpl
def menu_links(datasette, actor):
    if actor and actor.get("id") == "root":
        return [
            {
                "href": datasette.urls.path("/-/schema-versions"),
                "label": "Schema versions",
            },
        ]


@hookimpl
def register_routes():
    return [
        (r"^/-/schema-versions$", schema_versions),
        (r"^/-/schema-versions\.json$", schema_versions_json),
    ]
