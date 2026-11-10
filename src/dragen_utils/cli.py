from importlib.metadata import version as package_version
from typing import Annotated

import typer

from dragen_utils import dx_qc, fastq_list, igv_session

cli = typer.Typer()
cli.add_typer(fastq_list.cli)
cli.add_typer(dx_qc.cli)
cli.add_typer(igv_session.cli)


def _version_callback(show_version: bool) -> None:
    """Version callback for the CLI. If `show_version` is True, prints the package version and exits.
    The Nextflow modules capture this output into their `versions` topic, so it must be the bare version and nothing else.

    Args:
        show_version: Whether to show the version and exit.

    """
    if show_version:
        typer.echo(package_version("dragen-utils"))
        raise typer.Exit()


@cli.callback()
def _cli_options(
    version: Annotated[
        bool, typer.Option("--version", callback=_version_callback, is_eager=True, help="Show the package version and exit.")
    ] = False,
) -> None:
    """Dragen-utils is a collection of utilities for working with Illumina DRAGEN."""
    pass


if __name__ == "__main__":
    cli()
