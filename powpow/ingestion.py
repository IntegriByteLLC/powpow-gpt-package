# import os
# import json
# import asyncio
# import asyncpg
# from powpow.processor import Processor
#
#
# class DataIngestion:
#     def __init__(self, db_config, api_key, table_name="records", use_remote = True, column_names=None, embedding_columns=None,embed_from=None):
#         """
#         Initialize data ingestion handler.
#
#         :param db_config: Dictionary with database credentials.
#         :param api_key: OpenAI API key.
#         :param table_name: Name of the database table.
#         :param column_names: List of column names to create.
#         :param embedding_columns: List of column names that should be embedded.
#         """
#         self.db_config = db_config
#         self.processor = Processor(api_key,use_remote)
#         self.table_name = table_name
#
#         if column_names:
#             self.column_names = column_names
#         else:
#             raise ValueError("You must define at least one column.")
#
#         # Ensure embedding_columns is a subset of column_names.
#         if embedding_columns:
#             self.embedding_columns = set(embedding_columns) & set(self.column_names)
#         else:
#             self.embedding_columns = set()
#         self.embed_from = embed_from
#         if self.embed_from:
#             if "lookup" not in self.column_names:
#                 self.column_names.append("lookup")
#
#     async def create_table(self, conn):
#         """
#         Drops the table if it exists and creates a new table with user-defined columns.
#         For the "lookup" column, the type is set to VECTOR(1536); all other columns use TEXT.
#         """
#         # Ensure the pgvector extension exists.
#         await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
#
#         # Drop table if it exists.
#         await conn.execute(f"DROP TABLE IF EXISTS {self.table_name};")
#         print(f"Dropped table `{self.table_name}` if it existed.")
#
#         # Build column definitions.
#         column_definitions = []
#         for col in self.column_names:
#             if col == "lookup":
#                 column_definitions.append(f'"{col}" VECTOR(1536)')
#             else:
#                 column_definitions.append(f'"{col}" TEXT')
#
#         # Create the table; assume "url" is unique.
#         create_table_query = f"""
#            CREATE TABLE {self.table_name} (
#                id SERIAL PRIMARY KEY,
#                {", ".join(column_definitions)},
#                UNIQUE("url")
#            );
#            """
#         await conn.execute(create_table_query)
#         print(f"Table `{self.table_name}` created with columns: {self.column_names}")
#
#     async def process_json_file(self, json_file):
#         """
#         Processes and inserts data from a JSON file into the database.
#         The JSON file should either be a list of objects or a dictionary (whose values are objects).
#         Each record must be a dictionary. The embedding is generated from the column specified in embed_from
#         and stored in the "lookup" column.
#         """
#         conn = await asyncpg.connect(**self.db_config)
#         await self.create_table(conn)
#
#         with open(json_file, "r", encoding="utf-8") as file:
#             data = json.load(file)
#
#         if isinstance(data, dict):
#             records = data.values()
#         elif isinstance(data, list):
#             records = data
#         else:
#             print("Invalid JSON structure.")
#             await conn.close()
#             return
#
#         for record in records:
#             if not isinstance(record, dict):
#                 print("Skipping record: not a valid JSON object.")
#                 continue
#
#             # Build a values list corresponding to self.column_names.
#             # For each column:
#             #   - If it's "lookup", then generate an embedding from the embed_from column.
#             #   - Otherwise, use the value from the record (or "N/A" if missing).
#             values = []
#             skip_record = False
#
#             for col in self.column_names:
#                 if col == "lookup":
#                     # Generate embedding from the designated text column.
#                     if not self.embed_from:
#                         # If no embedding source is provided, set lookup to NULL.
#                         values.append(None)
#                     else:
#                         text_val = record.get(self.embed_from, "")
#                         embedding = await self.processor.generate_embedding(text_val)
#                         if embedding is None or len(embedding) != 1536:
#                             print(
#                                 f"Skipping record for URL {record.get('url', 'N/A')}: invalid embedding from '{self.embed_from}'.")
#                             skip_record = True
#                             break
#                         emb_str = f"[{', '.join(map(str, embedding))}]"
#                         values.append(emb_str)
#                 else:
#                     # For other columns, use the record value; default to "N/A" if missing.
#                     values.append(record.get(col, "N/A"))
#
#             if skip_record:
#                 continue
#
#             # Build the INSERT query dynamically.
#             columns_sql = ", ".join(f'"{col}"' for col in self.column_names)
#             placeholders = ", ".join(f"${i + 1}" for i in range(len(values)))
#             # Use "url" as the unique key.
#             query = f"""
#                INSERT INTO {self.table_name} ({columns_sql})
#                VALUES ({placeholders})
#                ON CONFLICT ("url") DO UPDATE
#                SET {", ".join(f'"{col}" = EXCLUDED."{col}"' for col in self.column_names if col != "url")};
#                """
#             try:
#                 await conn.execute(query, *values)
#                 print(f"Inserted/Updated record for URL: {record.get('url', 'N/A')}")
#             except Exception as e:
#                 print(f"Error processing record with URL {record.get('url', 'N/A')}: {e}")
#
#         await conn.close()
#         print(f"Completed processing {json_file}.")
#
#     async def process_all_json_files(self, directory):
#         """
#         Processes all JSON files in a directory.
#
#         :param directory: Path to the directory containing JSON files.
#         """
#         for file_name in os.listdir(directory):
#             if file_name.endswith(".json"):
#                 json_file = os.path.join(directory, file_name)
#                 print(f"Processing {json_file} with columns: {self.column_names}")
#                 await self.process_json_file(json_file)
