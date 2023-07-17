import nbformat as nbf
import logging
from pathlib import Path


# set the config for logging and create logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# def read_notebook(notebook_path):
#     with open(notebook_path, 'r', encoding='utf-8') as f:
#         notebook = nbf.read(f, as_version=4)


#     cells = []
#     md_cells = []
#     code_cells = [] 
#     md_id_to_cell_id = {}  # i-th element of md_cells corresponds to which element in cells?
#     code_id_to_cell_id = {}  # i-th element of code_cells corresponds to which element in cells?

#     for cell in notebook.cells:
#         cells.append(cell.source)
#         if cell.cell_type == 'markdown':
#             md_cells.append(cell.source)
#             md_id_to_cell_id[len(md_cells) - 1] = len(cells) - 1
#         elif cell.cell_type == 'code':
#             code_cells.append(cell.source)
#             code_id_to_cell_id[len(code_cells) - 1] = len(cells) - 1

#     return md_cells, code_cells, md_id_to_cell_id, code_id_to_cell_id


def read_nbs(repo):
    logger.info(f"Reading jupyter notebooks from {repo}")
    nb_dir = Path(f"docs/{repo}")
    nb_paths = list(nb_dir.rglob("*.ipynb"))
    md_cells, code_cells, cells = [], [], []
    md_id_to_cell_id, code_id_to_cell_id = {}, {}

    for np_path in nb_paths:
        # md_cells, code_cells, md_id_to_cell_id, code_id_to_cell_id = read_notebook(doc_p)
        with open(np_path, 'r', encoding='utf-8') as f:
            nb = nbf.read(f, as_version=4)
        for cell in nb.cells:
            cells.append(cell.source)
            if cell.cell_type == 'markdown':
                md_cells.append(cell.source)
                md_id_to_cell_id[len(md_cells) - 1] = len(cells) - 1
            elif cell.cell_type == 'code':
                code_cells.append(cell.source) 
                code_id_to_cell_id[len(code_cells) - 1] = len(cells) - 1

    return md_cells, code_cells, md_id_to_cell_id, code_id_to_cell_id


if __name__ == "__main__":
    read_nbs("llama_index")
    # md_cells, code_cells = read_nbs("llama_index")
    # md, code = read_notebook("docs/llama_index/examples/query_engine/SQLAutoVectorQueryEngine.ipynb")
    # for el in code:
    #     print(el)
    #     print("\n\n")
    # for el in md_cells:
    #     print(el)
    #     print("\n\n")