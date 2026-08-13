from pathlib import Path

from dragen_utils.dx_qc import main, parse_dragen_metrics_csv, transform_karyotype_value


def test_parse_dragen_metrics_csv() -> None:
    test_csv = Path("tests/data/dx_qc/HG002.wgs_coverage_metrics.csv")

    result = parse_dragen_metrics_csv(test_csv, "Average alignment coverage over genome")

    assert result == "51.29"


def test_transform_karyotype_value() -> None:

    assert transform_karyotype_value("XX") == "Vrouw"
    assert transform_karyotype_value("XY") == "Man"
    assert transform_karyotype_value("XXY") == "Man"
    assert transform_karyotype_value("XYY") == "Man"
    assert transform_karyotype_value("X0") == "Vrouw"
    assert transform_karyotype_value("XXXY") == "Man"
    assert transform_karyotype_value("XXX") == "Vrouw"
    assert transform_karyotype_value("") == "Onbekend"
    assert transform_karyotype_value(None) == "Onbekend"


def test_main(capsys) -> None:
    sample_id = "HG002"
    coverage_metrics_csv = Path("tests/data/dx_qc/HG002.wgs_coverage_metrics.csv")
    cnv_metrics_csv = Path("tests/data/dx_qc/HG002.cnv_metrics.csv")
    mapping_metrics_csv = Path("tests/data/dx_qc/HG002.mapping_metrics.csv")
    ploidy_estimation_metrics_csv = Path("tests/data/dx_qc/HG002.ploidy_estimation_metrics.csv")
    callability_metrics_csv = Path("tests/data/dx_qc/HG002.gvcf_metrics.csv")

    main(
        sample_id,
        coverage_metrics_csv,
        cnv_metrics_csv,
        mapping_metrics_csv,
        ploidy_estimation_metrics_csv,
        callability_metrics_csv,
    )

    assert capsys.readouterr().out == (
        "Sample ID,Average Coverage,CNV Coverage Uniformity,Contamination,Determined Sex,Percent Autosome Callability\n"
        "HG002,51.29,0.30,0.0000,Man,97.7178\n"
    )
