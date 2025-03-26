# import os
# from dotenv import load_dotenv
#
# # Load environment variables from .env
# load_dotenv()
#
# class Env:
#     """
#     A utility class to manage environment variables with proper type handling.
#     """
#
#     @staticmethod
#     def get(key: str, default: str = None) -> str:
#         """Retrieve a string environment variable with a default fallback."""
#         return os.getenv(key, default)
#
#     @staticmethod
#     def get_int(key: str, default: int = 0) -> int:
#         """Retrieve an integer environment variable."""
#         try:
#             return int(os.getenv(key, default))
#         except ValueError:
#             return default
#
#     @staticmethod
#     def get_bool(key: str, default: bool = False) -> bool:
#         """Retrieve a boolean environment variable."""
#         value = os.getenv(key, str(default)).lower()
#         return value in ["true", "1", "yes"]
#
