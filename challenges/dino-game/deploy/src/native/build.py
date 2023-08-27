from typing import Any

from pybind11.setup_helpers import Pybind11Extension, build_ext


def build(setup_kwargs: dict[str, Any]):
    ext_modules = [
        Pybind11Extension(
            "license_checker",
            ["src/main.cpp"],
            extra_compile_args=["-O3"],
            extra_link_args=["-s"],
        ),
    ]
    setup_kwargs.update(
        {
            "ext_modules": ext_modules,
            "cmd_class": {"build_ext": build_ext},
            "zip_safe": False,
        }
    )
