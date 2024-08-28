import os

from pinecone import Pinecone

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "quickstart"
index = pc.Index(index_name)

# index.upsert(
#     vectors=[
#         {"id": "vec1", "values": [1.0, 1.5]},
#         {"id": "vec2", "values": [2.0, 1.0]},
#         {"id": "vec3", "values": [0.1, 3.0]},
#     ],
#     namespace="ns1"
# )
#
# index.upsert(
#     vectors=[
#         {"id": "vec1", "values": [1.0, -2.5]},
#         {"id": "vec2", "values": [3.0, -2.0]},
#         {"id": "vec3", "values": [0.5, -1.5]},
#     ],
#     namespace="ns2"
# )


index.upsert(
    vectors=[
        {"id": "vec4", "values": [1.1, 1.8]},
        {"id": "vec5", "values": [3.0, 2.0]},
        {"id": "vec6", "values": [0.16, 3.6]},
    ],
    namespace="ns1"
)

index.upsert(
    vectors=[
        {"id": "vec4", "values": [1.3, -2.9]},
        {"id": "vec5", "values": [3.2, -2.1]},
        {"id": "vec6", "values": [0.6, -1.8]},
    ],
    namespace="ns2"
)