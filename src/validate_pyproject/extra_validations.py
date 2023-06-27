"""The purpose of this module is implement PEP 621 validations that are
difficult to express as a JSON Schema (or that are not supported by the current
JSON Schema library).
"""

from inspect import cleandoc
from typing import Mapping, TypeVar

from .error_reporting import ValidationError

T = TypeVar("T", bound=Mapping)


class RedefiningStaticFieldAsDynamic(ValidationError):
    """According to PEP 621:

    Build back-ends MUST raise an error if the metadata specifies a field
    statically as well as being listed in dynamic.
    """

    _URL = (
        "https://packaging.python.org/en/latest/specifications/"
        "declaring-project-metadata/#dynamic"
    )


def validate_project_dynamic(pyproject: T) -> T:
    project_table = pyproject.get("project", {})
    dynamic = project_table.get("dynamic", [])

    for field in dynamic:
        if field in project_table:
            raise RedefiningStaticFieldAsDynamic(
                message=f"You cannot provide a value for `project.{field}` and "
                "list it under `project.dynamic` at the same time",
                value={
                    field: project_table[field],
                    "...": " # ...",
                    "dynamic": dynamic,
                },
                name=f"data.project.{field}",
                definition={
                    "description": cleandoc(RedefiningStaticFieldAsDynamic.__doc__),
                    "see": RedefiningStaticFieldAsDynamic._URL,
                },
                rule="PEP 621",
            )

    return pyproject


EXTRA_VALIDATIONS = (validate_project_dynamic,)
