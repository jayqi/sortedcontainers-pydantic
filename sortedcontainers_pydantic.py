from collections.abc import Mapping
from typing import Any, Iterable, Set, Tuple, get_args

from pydantic import (
    GetCoreSchemaHandler,
)
from pydantic_core import core_schema
import sortedcontainers

__version__ = "1.0.0"


class SortedDict(sortedcontainers.SortedDict):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        """
        Returns pydantic_core.CoreSchema that defines how Pydantic should validate and
        serialize this class.

        - Validating from JSON: Validate as an iterable and pass to SortedList
          constructor
        - Validating from Python:
            - If it's already a SortedList, do nothing
            - If it's an iterable, pass to SortedList constructor
        - Serialization: Convert to a list
        """
        # Schema for when the input is already an instance of this class
        instance_schema = core_schema.is_instance_schema(cls)

        # Get schema for Iterable type based on source type has arguments
        args = get_args(source_type)
        if args:
            mapping_t_schema = handler.generate_schema(Mapping[*args])  # type: ignore
            iterable_of_pairs_t_schema = handler.generate_schema(Iterable[Tuple[*args]])  # type: ignore
        else:
            mapping_t_schema = handler.generate_schema(Mapping)
            iterable_of_pairs_t_schema = handler.generate_schema(Iterable[Tuple[Any, Any]])

        # Schema for when the input is a mapping
        from_mapping_schema = core_schema.no_info_after_validator_function(
            function=cls, schema=mapping_t_schema
        )

        # Schema for when the input is an iterable of pairs
        from_iterable_of_pairs_schema = core_schema.no_info_after_validator_function(
            function=cls, schema=iterable_of_pairs_t_schema
        )

        # Union of the two schemas
        python_schema = core_schema.union_schema(
            [
                instance_schema,
                from_mapping_schema,
                from_iterable_of_pairs_schema,
            ]
        )

        # Serializer that converts an instance to a dict
        as_dict_serializer = core_schema.plain_serializer_function_ser_schema(dict)

        return core_schema.json_or_python_schema(
            json_schema=from_mapping_schema,
            python_schema=python_schema,
            serialization=as_dict_serializer,
        )


class SortedList(sortedcontainers.SortedList):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        """
        Returns pydantic_core.CoreSchema that defines how Pydantic should validate and
        serialize this class.

        - Validating from JSON: Validate as an iterable and pass to SortedList
          constructor
        - Validating from Python:
            - If it's already a SortedList, do nothing
            - If it's an iterable, pass to SortedList constructor
        - Serialization: Convert to a list
        """
        # Schema for when the input is already an instance of this class
        instance_schema = core_schema.is_instance_schema(cls)

        # Get schema for Iterable type based on source type has arguments
        args = get_args(source_type)
        if args:
            iterable_t_schema = handler.generate_schema(Iterable[*args])  # type: ignore
        else:
            iterable_t_schema = handler.generate_schema(Iterable)

        # Schema for when the input is an iterable
        from_iterable_schema = core_schema.no_info_after_validator_function(
            function=cls, schema=iterable_t_schema
        )

        # Union of the two schemas
        python_schema = core_schema.union_schema(
            [
                instance_schema,
                from_iterable_schema,
            ]
        )

        # Serializer that converts an instance to a list
        as_list_serializer = core_schema.plain_serializer_function_ser_schema(list)

        return core_schema.json_or_python_schema(
            json_schema=from_iterable_schema,
            python_schema=python_schema,
            serialization=as_list_serializer,
        )


class SortedSet(sortedcontainers.SortedSet):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        """
        Returns pydantic_core.CoreSchema that defines how Pydantic should validate and
        serialize this class.

        - Validating from JSON: Validate as an iterable and pass to SortedSet
          constructor
        - Validating from Python:
            - If it's already a SortedSet, do nothing
            - If it's a set, parse as a set and pass to SortedSet constructor
            - If it's an iterable, pass to SortedSet constructor
        - Serialization: Convert to a list
        """
        # Schema for when the input is already an instance of this class
        instance_schema = core_schema.is_instance_schema(cls)

        # Get schema for Iterable type based on source type has arguments
        args = get_args(source_type)
        if args:
            set_t_schema = handler.generate_schema(Set[*args])  # type: ignore
            iterable_t_schema = handler.generate_schema(Iterable[*args])  # type: ignore
        else:
            set_t_schema = handler.generate_schema(Set)
            iterable_t_schema = handler.generate_schema(Iterable)

        # Schema for when the input is a set
        from_set_schema = core_schema.no_info_after_validator_function(
            function=cls, schema=set_t_schema
        )

        # Schema for when the input is an iterable
        from_iterable_schema = core_schema.no_info_after_validator_function(
            function=cls, schema=iterable_t_schema
        )

        # Union of the two schemas
        python_schema = core_schema.union_schema(
            [
                instance_schema,
                from_set_schema,
                from_iterable_schema,
            ]
        )

        # Serializer that converts an instance to a set
        as_set_serializer = core_schema.plain_serializer_function_ser_schema(set)

        return core_schema.json_or_python_schema(
            json_schema=from_set_schema,
            python_schema=python_schema,
            serialization=as_set_serializer,
        )
