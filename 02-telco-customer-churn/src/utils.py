# src/utils.py

"""
Utility functions used throughout the project.

Functions:
----------
create_directory()
save_pickle()
load_pickle()
save_dataframe()
save_figure()
"""

from pathlib import Path
import pickle
import pandas as pd


def create_directory(directory_path):
    """
    Create a directory if it does not exist.

    Parameters
    ----------
    directory_path : str
        Path to directory.

    Returns
    -------
    pathlib.Path
        Created directory path.
    """

    path = Path(directory_path)

    path.mkdir(
        parents=True,
        exist_ok=True
    )

    return path


def save_pickle(
    obj,
    file_path
):
    """
    Save Python object as pickle file.

    Parameters
    ----------
    obj : any
        Object to save.

    file_path : str
        Output file path.
    """

    file_path = Path(file_path)

    create_directory(
        file_path.parent
    )

    with open(
        file_path,
        "wb"
    ) as file:

        pickle.dump(
            obj,
            file
        )

    print(
        f"Object saved to: {file_path}"
    )


def load_pickle(
    file_path
):
    """
    Load pickle file.

    Parameters
    ----------
    file_path : str
        Pickle file path.

    Returns
    -------
    object
        Loaded object.
    """

    with open(
        file_path,
        "rb"
    ) as file:

        return pickle.load(file)


def save_dataframe(
    dataframe,
    file_path,
    index=False
):
    """
    Save DataFrame to CSV.

    Parameters
    ----------
    dataframe : pd.DataFrame

    file_path : str

    index : bool
        Whether to save index.
    """

    file_path = Path(file_path)

    create_directory(
        file_path.parent
    )

    dataframe.to_csv(
        file_path,
        index=index
    )

    print(
        f"DataFrame saved to: {file_path}"
    )


def save_figure(
    file_path,
    dpi=300,
    bbox_inches="tight"
):
    """
    Save current matplotlib figure.

    Parameters
    ----------
    file_path : str

    dpi : int

    bbox_inches : str
    """

    from matplotlib import pyplot as plt

    file_path = Path(file_path)

    create_directory(
        file_path.parent
    )

    plt.savefig(
        file_path,
        dpi=dpi,
        bbox_inches=bbox_inches
    )

    print(
        f"Figure saved to: {file_path}"
    )


def export_results(
    dataframe,
    output_path
):
    """
    Save evaluation results.
    """

    dataframe.to_csv(
        output_path,
        index=False
    )
