"""Module contain custom pydantic types."""
from __future__ import annotations

import typing as t

from click.types import CompletionItem, Context, Parameter, ParamType
from pydantic.fields import FieldInfo, Undefined

# TypeAlias and list as generic import from future.
TClickType: t.TypeAlias = t.Union[t.Any, ParamType, None]  # type: ignore
_TClickShellComplete: t.TypeAlias = t.Callable[  # type: ignore
    [Context, Parameter, str],
    t.Union[list[CompletionItem], list[str]],  # type: ignore [misc]
]


class _ClickBaseParameter(FieldInfo):
    """Base click parameter as pydantic field.

    Attributes:
        __param_decls__: Base parameter declarations.

        _click_data: Storage click parameter settings.
        _click_type: Storage click type settings.

    Args:
        pydantic_field_params: Pydantic field parameters.

    """

    __slots__ = ("_click_data",)

    __param_decls__: t.ClassVar[tuple[str, ...]] = tuple()

    _click_data: dict[str, t.Any]
    _click_decls: t.Sequence[str] | str
    _click_type: TClickType

    def __init__(
        self,
        required: bool | None = None,
        default: t.Any | t.Callable[[], t.Any] | None = None,
        callback: t.Callable[[Context, Parameter, t.Any], t.Any] | None = None,
        nargs: int | None = None,
        multiple: bool = False,
        metavar: str | None = None,
        expose_value: bool = True,
        is_eager: bool = False,
        envvar: str | t.Sequence[str] | None = None,
        shell_complete: _TClickShellComplete | None = None,
        **pydantic_data: t.Any,
    ) -> None:
        """Override initialization of pydantic Field.
        Added param_decls as args parameter.
        """

        # Update click data py core click parameter data.
        self.click_data = dict(
            required=required,
            default=default,
            callback=callback,
            nargs=nargs,
            multiple=multiple,
            metavar=metavar,
            expose_value=expose_value,
            is_eager=is_eager,
            envvar=envvar,
            shell_complete=shell_complete,
        )

        pydantic_data = self._get_pydantic_field_data(**pydantic_data)

        super().__init__(**pydantic_data)
        self._validate()

    def __repr__(self) -> str:
        """Representation of Click parameter class."""

        return f"<{self.__class__.__name__}> data={self._click_data}"

    @property
    def click_type(self) -> TClickType:
        """Get click type of parameter."""

        return self._click_type

    @click_type.setter
    def click_type(self, type_: TClickType) -> None:
        """Set click type parameter."""

        self._click_type = type_

    @property
    def click_data(self) -> dict[str, t.Any]:
        """Get click data of parameter."""

        return self._click_data

    @click_data.setter
    def click_data(self, data: dict[str, t.Any]) -> None:
        """Set or update click data."""

        if "_click_data" in self.__dict__:
            self._click_data.update(data)
        else:
            self._click_data = data

    @property
    def click_decls(self) -> t.Sequence[str]:
        """Get click parameter decls."""

        return self._click_decls

    @click_decls.setter
    def click_decls(self, decls: t.Sequence[str]) -> None:
        """Set or update click decls."""

        if "_click_decls" in self.__dict__:
            new_decls = [
                decl for decl in decls if decl not in self._click_decls
            ]
        else:
            new_decls = list(self.__param_decls__)
            new_decls.extend(
                [decl for decl in decls if decl not in self.__param_decls__]
            )

        self._click_decls = new_decls

    def _get_pydantic_field_data(self, **params) -> dict[str, t.Any]:
        """Compare click parameter data who cross with pydantic field data."""

        # Set default.
        default = self.click_data.get("default", Undefined)
        if callable(default) and "default_factory" not in params:
            params["default_factory"] = default
        else:
            params["default"] = default

        # Set description.
        descr = self.click_data.get("help")
        if "description" not in params and descr:
            params["description"] = descr

        # Set min and max items.
        nargs = self.click_data.get("nargs", 1)
        if nargs > 1:
            params["min_items"] = nargs
            params["max_items"] = nargs

        return params


class Argument(_ClickBaseParameter):
    """Click argument implementation as pydantic field.

    Args:
        params: other click and pydantic parameters.

    """

    def __init__(
        self,
        required: bool | None = None,
        default: t.Any | t.Callable[[], t.Any] | None = None,
        nargs: int | None = None,
        envvar: str | t.Sequence[str] | None = None,
        **params: t.Any,
    ) -> None:
        super().__init__(
            required=required,
            default=default,
            nargs=nargs,
            envvar=envvar,
            **params,
        )


class Option(_ClickBaseParameter):
    """Click option argument implementation as pydantic field.

    Args:
        params: other click and pydantic parameters.

    """

    def __init__(
        self,
        *param_decls: str,
        required: bool | None = None,
        default: t.Any | t.Callable[[], t.Any] | None = None,
        nargs: int | None = None,
        multiple: bool = False,
        callback: t.Callable[[Context, Parameter, t.Any], t.Any] | None = None,
        expose_value: bool = True,
        is_eager: bool = False,
        envvar: str | t.Sequence[str] | None = None,
        show_default: bool | str | None = None,
        count: bool = False,
        is_flag: bool | None = None,
        flag_value: t.Any | None = None,
        prompt: bool | str = False,
        confirmation_prompt: bool | str = False,
        hide_input: bool = False,
        help: str | None = None,
        prompt_required: bool = True,
        allow_from_autoenv: bool = True,
        hidden: bool = False,
        show_choices: bool = True,
        show_envvar: bool = False,
        **params: t.Any,
    ) -> None:

        self.click_decls = param_decls
        self.click_data = dict(
            show_default=show_default,
            prompt=prompt,
            confirmation_prompt=confirmation_prompt,
            prompt_required=prompt_required,
            hide_input=hide_input,
            is_flag=is_flag,
            flag_value=flag_value,
            count=count,
            allow_from_autoenv=allow_from_autoenv,
            help=help,
            hidden=hidden,
            show_choices=show_choices,
            show_envvar=show_envvar,
        )

        super().__init__(
            required=required,
            default=default,
            nargs=nargs,
            multiple=multiple,
            callback=callback,
            expose_value=expose_value,
            is_eager=is_eager,
            envvar=envvar,
            **params,
        )
