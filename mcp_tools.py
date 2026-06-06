import requests
from crewai.tools import BaseTool

MCP_URL = "http://127.0.0.1:8080/mcp"

class ReadCSVTool(BaseTool):

    name: str = "Read CSV Tool"

    description: str = "Reads a CSV preview"

    def _run(self):

        response = requests.post(
            f"{MCP_URL}/tools/file_read_csv",
            json={
                "sample":90
            }
        )

        return response.json()

class ComputeStatsTool(BaseTool):

    name: str = "Compute Stats Tool"

    description: str = """
    Compute statistics for a column.

    Arguments:
      rows (list): rows of data
      column (str): column name
    """

    def _run(self, rows, column):

        response = requests.post(
            f"{MCP_URL}/tools/compute_stats",
            json={
                "rows": rows,
                "column": column
            }
        )

        return response.json()
