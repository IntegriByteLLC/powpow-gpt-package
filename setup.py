from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

setup(
    name="powpow_gpt",
    version="0.1.0",
    author="iNTEGRiBYTE",
    author_email="randyp@integri-byte.com",
    description="A secure and compiled AI assistant package",
    long_description="Full Cython-powered RAG package with OpenAI + pgvector support.",
    url="https://github.com/IntegriByteLLC/powpow-gpt-package",
    project_urls={
        "Source": "https://github.com/IntegriByteLLC/powpow-gpt-package"
    },
    packages=find_packages(),
    include_package_data=True,
    # ext_modules=cythonize(
    #     [
    #         Extension("powpow_gpt.processor", ["powpow_gpt/processor.pyx"]),
    #         Extension("powpow_gpt.database", ["powpow_gpt/database.pyx"]),
    #         Extension("powpow_gpt.ingestion", ["powpow_gpt/ingestion.pyx"]),
    #         Extension("powpow_gpt.gpt_assistant", ["powpow_gpt/gpt_assistant.pyx"]),
    #         Extension("powpow_gpt.config", ["powpow_gpt/config.pyx"]),
    #         Extension("powpow_gpt.logger", ["powpow_gpt/logger.pyx"]),
    #         Extension("powpow_gpt.env", ["powpow_gpt/env.pyx"]),
    #     ],
    #     language_level="3",
    # ),
    zip_safe=False,
)

#
# token="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"
