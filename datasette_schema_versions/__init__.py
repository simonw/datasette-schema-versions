from datasette import hookimpl
from datasette.utils.asgi import Response


async def schema_versions(datasette):
    schema_versions = {}
    for name, database in datasette.databases.items():
        schema_versions[name] = (
            await database.execute("PRAGMA schema_version")
        ).first()[0]
    return Response.json(schema_versions)


@hookimpl
def register_routes():
    return [("^/-/schema-versions$", schema_versions)]
