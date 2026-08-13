import gzip
from pathlib import Path

import typer

cli = typer.Typer()


def get_fastq_metadata(fastq_file: Path) -> dict:
    """Extract metadata from a fastq file.

    Args:
        fastq_file: Path to the fastq file.

    Returns:
        Dictionary containing sample ID, machine, run, flowcell, and lane.
    """
    sample_id = fastq_file.name.split("_")[0]

    with gzip.open(fastq_file, "rt") as f:
        fastq_data = f.readline().strip().split(":")
        machine, run, flowcell, lane = fastq_data[0:4]

    return {
        "sample_id": sample_id,
        "machine": machine,
        "run": run,
        "flowcell": flowcell,
        "lane": lane,
    }


def get_rg_id(fastq_metadata: dict) -> str:
    """Generate a read group ID based on fastq metadata.

    Args:
        fastq_metadata: Dictionary containing fastq metadata.

    Returns:
        Read group ID.
    """
    fastq_rg_id = "{sample_id}_{flowcell}_{lane}".format(
        sample_id=fastq_metadata["sample_id"],
        flowcell=fastq_metadata["flowcell"],
        lane=fastq_metadata["lane"],
    )
    return fastq_rg_id


def get_rg_lb(fastq_metadata: dict) -> str:
    """Generate a read group library based on fastq metadata.

    Args:
        fastq_metadata: Dictionary containing fastq metadata.

    Returns:
        Read group library.
    """
    fastq_rg_lb = "{sample_id}_{flowcell}".format(sample_id=fastq_metadata["sample_id"], flowcell=fastq_metadata["flowcell"])
    return fastq_rg_lb


@cli.command("fastq_list")
def main(directory: Path = Path(".")) -> None:
    """Main function to find fastq files and generate a CSV file with read group information.

    Args:
        directory: Directory to search for fastq files. Defaults to the current directory.
    """
    r1_fastq_files = sorted(directory.glob("*_R1_*.fastq.gz"))
    fastq_pairs = []

    for r1_fastq_file in r1_fastq_files:
        fastq_metadata = get_fastq_metadata(r1_fastq_file)
        fastq_pair = {
            "RGSM": fastq_metadata["sample_id"],
            "RGID": get_rg_id(fastq_metadata),
            "RGLB": get_rg_lb(fastq_metadata),
            "RGPL": "ILLUMINA",
            "Lane": fastq_metadata["lane"],
            "Read1File": r1_fastq_file.name,
            "Read2File": r1_fastq_file.name.replace("_R1_", "_R2_"),
        }
        fastq_pairs.append(fastq_pair)

    # Print header and fastq pairs in CSV format
    print("RGSM", "RGID", "RGLB", "RGPL", "Lane", "Read1File", "Read2File", sep=",")
    for fastq_pair in fastq_pairs:
        print(
            fastq_pair["RGSM"],
            fastq_pair["RGID"],
            fastq_pair["RGLB"],
            fastq_pair["RGPL"],
            fastq_pair["Lane"],
            fastq_pair["Read1File"],
            fastq_pair["Read2File"],
            sep=",",
        )


if __name__ == "__main__":
    main()
