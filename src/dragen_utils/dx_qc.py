"""Generate a QC summary CSV for diagnostic samples from DRAGEN metrics files."""

import csv
from pathlib import Path

import typer

cli = typer.Typer()


def parse_dragen_metrics_csv(metrics_csv: Path, metric_description: str) -> str:
    """Parse a DRAGEN metrics CSV file and extract the specified metric value.

    Args:
        metrics_csv: Path to the DRAGEN metrics CSV file.
        metric_description: Description of the metric to extract.

    Returns:
        The value of the specified metric.

    """
    # CSV does not have a header row, so we need to hardcode the indices
    csv_description_idx = 2
    csv_value_idx = 3

    with Path(metrics_csv).open("r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[csv_description_idx] == metric_description:
                return row[csv_value_idx]


def transform_karyotype_value(dragen_karyotype: str) -> str:
    """Transform DRAGEN ploidy estimation value karyotype to 'man', 'vrouw', or 'onbekend'. To avoid incidental findings.

    Args:
        dragen_karyotype: Karyotype string from DRAGEN.

    Returns:
        The translated sex label ('man', 'vrouw' or 'onbekend').
    """
    if not dragen_karyotype or dragen_karyotype.strip() == "":
        return "Onbekend"

    karyotype = dragen_karyotype.strip().upper()
    if "Y" in karyotype:
        return "Man"
    else:
        return "Vrouw"


@cli.command("dx_qc")
def main(
    sample_id: str,
    coverage_metrics_csv: Path,
    cnv_metrics_csv: Path,
    mapping_metrics_csv: Path,
    ploidy_estimation_metrics_csv: Path,
    callability_metrics_csv: Path,
) -> None:
    """Generate QC values used to assess the quality of a sample.

    Args:
        sample_id: Sample ID to use for output file naming.
        coverage_metrics_csv: Path to the coverage metrics CSV file.
        cnv_metrics_csv: Path to the CNV metrics CSV file.
        mapping_metrics_csv: Path to the mapping metrics CSV file.
        ploidy_estimation_metrics_csv: Path to the ploidy estimation metrics CSV file.
        callability_metrics_csv: Path to the gvcf metrics CSV file.
    """
    # Get QC values from DRAGEN metrics CSV files
    coverage = parse_dragen_metrics_csv(coverage_metrics_csv, "Average alignment coverage over genome")
    cnv_coverage_uniformity = parse_dragen_metrics_csv(cnv_metrics_csv, "Coverage uniformity")
    contamination = parse_dragen_metrics_csv(mapping_metrics_csv, "Estimated sample contamination")
    karyotype = parse_dragen_metrics_csv(ploidy_estimation_metrics_csv, "Ploidy estimation")
    autosome_callability = parse_dragen_metrics_csv(callability_metrics_csv, "Percent Autosome Callability")

    # Transform karyotype to sex label
    sex = transform_karyotype_value(karyotype)

    # Print Header and QC values in CSV format
    print(
        "Sample ID",
        "Average Coverage",
        "CNV Coverage Uniformity",
        "Contamination",
        "Determined Sex",
        "Percent Autosome Callability",
        sep=",",
    )
    print(sample_id, coverage, cnv_coverage_uniformity, contamination, sex, autosome_callability, sep=",")


if __name__ == "__main__":
    main()
