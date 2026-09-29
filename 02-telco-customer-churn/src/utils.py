"""
Reusable utility classes for file management, date handling,
and dataset inspection.

Classes
-------
FileManager
    Creates directories and manages CSV, Excel, JSON, pickle,
    and Matplotlib figure files.

DateUtils
    Generates formatted date and time values.

DataInspector
    Produces concise dataset quality summaries.
"""

from datetime import datetime
import json
import pickle
from pathlib import Path
from typing import Any, Mapping, Optional, Union

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure


PathLike = Union[str, Path]


class FileManager:
    """Provide reusable methods for reading and writing project files."""

    @staticmethod
    def _prepare_file_path(file_path: PathLike) -> Path:
        """
        Convert a file path to a Path object and create its parent directory.

        Parameters
        ----------
        file_path : str or pathlib.Path
            Destination file path.

        Returns
        -------
        pathlib.Path
            Prepared destination path.
        """
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        return path

    @staticmethod
    def create_directory(directory_path: PathLike) -> Path:
        """
        Create a directory, including any missing parent directories.

        Parameters
        ----------
        directory_path : str or pathlib.Path
            Directory to create.

        Returns
        -------
        pathlib.Path
            Prepared directory path.
        """
        path = Path(directory_path)
        path.mkdir(parents=True, exist_ok=True)

        return path

    @classmethod
    def save_dataframe(
        cls,
        dataframe: pd.DataFrame,
        file_path: PathLike,
        index: bool = False,
        **csv_options: Any,
    ) -> Path:
        """
        Save a DataFrame as a CSV file.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            DataFrame to save.
        file_path : str or pathlib.Path
            Destination CSV file path.
        index : bool, default=False
            Whether to include the DataFrame index.
        **csv_options
            Additional arguments passed to pandas.DataFrame.to_csv().

        Returns
        -------
        pathlib.Path
            Path of the saved CSV file.
        """
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("dataframe must be a pandas DataFrame.")

        path = cls._prepare_file_path(file_path)

        dataframe.to_csv(
            path,
            index=index,
            **csv_options,
        )

        return path

    @staticmethod
    def load_dataframe(
        file_path: PathLike,
        **csv_options: Any,
    ) -> pd.DataFrame:
        """
        Load a CSV file into a DataFrame.

        Parameters
        ----------
        file_path : str or pathlib.Path
            Source CSV file path.
        **csv_options
            Additional arguments passed to pandas.read_csv().

        Returns
        -------
        pandas.DataFrame
            Loaded dataset.

        Raises
        ------
        FileNotFoundError
            If the CSV file does not exist.
        """
        path = Path(file_path)

        if not path.is_file():
            raise FileNotFoundError(
                f"CSV file not found: {path}"
            )

        return pd.read_csv(
            path,
            **csv_options,
        )

    @classmethod
    def save_excel(
        cls,
        dataframes: Mapping[str, pd.DataFrame],
        file_path: PathLike,
        index: bool = False,
        engine: str = "openpyxl",
    ) -> Path:
        """
        Save one or more DataFrames in separate Excel worksheets.

        Parameters
        ----------
        dataframes : mapping of str to pandas.DataFrame
            Dictionary-like object containing worksheet names and
            their corresponding DataFrames.

            Example:
            {
                "Executive Summary": executive_summary,
                "Recommendations": recommendations,
            }

        file_path : str or pathlib.Path
            Destination Excel workbook path.

        index : bool, default=False
            Whether to include DataFrame indexes.

        engine : str, default="openpyxl"
            Excel writing engine.

        Returns
        -------
        pathlib.Path
            Path of the saved Excel workbook.

        Raises
        ------
        ValueError
            If the dataframes mapping is empty.

        TypeError
            If any worksheet value is not a DataFrame.
        """
        if not dataframes:
            raise ValueError(
                "dataframes cannot be empty."
            )

        path = cls._prepare_file_path(file_path)

        with pd.ExcelWriter(
            path,
            engine=engine,
        ) as writer:
            for sheet_name, dataframe in dataframes.items():
                if not isinstance(dataframe, pd.DataFrame):
                    raise TypeError(
                        f"Worksheet '{sheet_name}' must contain "
                        "a pandas DataFrame."
                    )

                dataframe.to_excel(
                    writer,
                    sheet_name=str(sheet_name)[:31],
                    index=index,
                )

        return path

    @classmethod
    def save_json(
        cls,
        data: Any,
        file_path: PathLike,
        indent: int = 4,
    ) -> Path:
        """
        Save JSON-compatible data to a file.

        Parameters
        ----------
        data : any
            JSON-compatible object to save.
        file_path : str or pathlib.Path
            Destination JSON file path.
        indent : int, default=4
            Number of spaces used for indentation.

        Returns
        -------
        pathlib.Path
            Path of the saved JSON file.
        """
        path = cls._prepare_file_path(file_path)

        with path.open(
            mode="w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                indent=indent,
                ensure_ascii=False,
                default=str,
            )

        return path

    @staticmethod
    def load_json(file_path: PathLike) -> Any:
        """
        Load data from a JSON file.

        Parameters
        ----------
        file_path : str or pathlib.Path
            Source JSON file path.

        Returns
        -------
        any
            Deserialized JSON data.

        Raises
        ------
        FileNotFoundError
            If the JSON file does not exist.
        """
        path = Path(file_path)

        if not path.is_file():
            raise FileNotFoundError(
                f"JSON file not found: {path}"
            )

        with path.open(
            mode="r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    @classmethod
    def save_pickle(
        cls,
        obj: Any,
        file_path: PathLike,
    ) -> Path:
        """
        Serialize a Python object as a pickle file.

        Parameters
        ----------
        obj : any
            Python object to save.
        file_path : str or pathlib.Path
            Destination pickle file path.

        Returns
        -------
        pathlib.Path
            Path of the saved pickle file.
        """
        path = cls._prepare_file_path(file_path)

        with path.open(mode="wb") as file:
            pickle.dump(
                obj,
                file,
                protocol=pickle.HIGHEST_PROTOCOL,
            )

        return path

    @staticmethod
    def load_pickle(file_path: PathLike) -> Any:
        """
        Load an object from a trusted pickle file.

        Parameters
        ----------
        file_path : str or pathlib.Path
            Source pickle file path.

        Returns
        -------
        any
            Deserialized Python object.

        Raises
        ------
        FileNotFoundError
            If the pickle file does not exist.

        Notes
        -----
        Pickle files can execute arbitrary code. Only load pickle
        files obtained from trusted sources.
        """
        path = Path(file_path)

        if not path.is_file():
            raise FileNotFoundError(
                f"Pickle file not found: {path}"
            )

        with path.open(mode="rb") as file:
            return pickle.load(file)

    @classmethod
    def save_figure(
        cls,
        file_path: PathLike,
        figure: Optional[Figure] = None,
        dpi: int = 300,
        bbox_inches: str = "tight",
        close: bool = False,
        **savefig_options: Any,
    ) -> Path:
        """
        Save a Matplotlib figure.

        If no figure is supplied, the current active figure is saved.

        Parameters
        ----------
        file_path : str or pathlib.Path
            Destination image path.

        figure : matplotlib.figure.Figure, optional
            Figure to save. If omitted, matplotlib.pyplot.gcf()
            provides the active figure.

        dpi : int, default=300
            Image resolution in dots per inch.

        bbox_inches : str, default="tight"
            Bounding-box setting passed to Figure.savefig().

        close : bool, default=False
            Whether to close the figure after saving it.

        **savefig_options
            Additional arguments passed to Figure.savefig().

        Returns
        -------
        pathlib.Path
            Path of the saved figure.
        """
        path = cls._prepare_file_path(file_path)

        selected_figure = (
            figure
            if figure is not None
            else plt.gcf()
        )

        selected_figure.savefig(
            path,
            dpi=dpi,
            bbox_inches=bbox_inches,
            **savefig_options,
        )

        if close:
            plt.close(selected_figure)

        return path


class DateUtils:
    """Provide consistent date and timestamp formatting."""

    @staticmethod
    def create_timestamp(
        format_string: str = "%Y%m%d_%H%M%S",
    ) -> str:
        """
        Return the current local date and time as a formatted string.

        Parameters
        ----------
        format_string : str, default="%Y%m%d_%H%M%S"
            Date and time format accepted by datetime.strftime().

        Returns
        -------
        str
            Formatted timestamp.
        """
        return datetime.now().strftime(format_string)


class DataInspector:
    """Provide lightweight dataset structure and quality checks."""

    @staticmethod
    def _validate_dataframe(
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Validate that an object is a pandas DataFrame.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            Object to validate.

        Raises
        ------
        TypeError
            If the supplied object is not a DataFrame.
        """
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError(
                "dataframe must be a pandas DataFrame."
            )

    @classmethod
    def dataset_summary(
        cls,
        dataframe: pd.DataFrame,
    ) -> pd.Series:
        """
        Return structural and quality indicators for a DataFrame.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            Dataset to inspect.

        Returns
        -------
        pandas.Series
            Summary containing:

            - number of rows
            - number of columns
            - duplicate rows
            - missing values
            - memory usage in megabytes
        """
        cls._validate_dataframe(dataframe)

        return pd.Series(
            {
                "rows": dataframe.shape[0],
                "columns": dataframe.shape[1],
                "duplicate_rows": int(
                    dataframe.duplicated().sum()
                ),
                "missing_values": int(
                    dataframe.isna().sum().sum()
                ),
                "memory_mb": round(
                    dataframe.memory_usage(
                        deep=True
                    ).sum()
                    / 1_048_576,
                    3,
                ),
            },
            name="dataset_summary",
        )

    @classmethod
    def missing_values(
        cls,
        dataframe: pd.DataFrame,
        include_complete: bool = False,
    ) -> pd.DataFrame:
        """
        Summarize missing values by column.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            Dataset to inspect.

        include_complete : bool, default=False
            Whether to include columns without missing values.

        Returns
        -------
        pandas.DataFrame
            Missing-value counts and percentages for each column.
        """
        cls._validate_dataframe(dataframe)

        missing_count = dataframe.isna().sum()

        if dataframe.empty:
            missing_percentage = pd.Series(
                0.0,
                index=dataframe.columns,
            )
        else:
            missing_percentage = (
                missing_count
                .div(len(dataframe))
                .mul(100)
                .round(2)
            )

        summary = pd.DataFrame(
            {
                "missing_count": missing_count,
                "missing_percentage": missing_percentage,
            }
        )

        if not include_complete:
            summary = summary.loc[
                summary["missing_count"] > 0
            ]

        return summary.sort_values(
            by=[
                "missing_percentage",
                "missing_count",
            ],
            ascending=False,
        )