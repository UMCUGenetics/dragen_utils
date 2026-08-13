import typer

from dragen_utils import dx_qc, fastq_list

cli = typer.Typer()
cli.add_typer(fastq_list.cli)
cli.add_typer(dx_qc.cli)

if __name__ == "__main__":
    cli()
