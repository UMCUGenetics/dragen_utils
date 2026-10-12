from pathlib import Path

from pytest_mock import MockerFixture
from typer.testing import CliRunner

from dragen_utils import cli, dx_qc, fastq_list

runner = CliRunner()


def test_fastq_list(mocker: MockerFixture) -> None:
    """Test that the fastq_list command is registered and can be invoked."""
    command = next(command for command in fastq_list.cli.registered_commands if command.name == "fastq_list")
    mock_callback = mocker.patch.object(command, "callback", autospec=True)

    result = runner.invoke(cli.cli, ["fastq_list"])

    assert result.exit_code == 0
    mock_callback.assert_called_once_with(directory=Path())


def test_dx_qc(mocker: MockerFixture) -> None:
    """Test that the dx_qc command is registered and can be invoked."""
    command = next(command for command in dx_qc.cli.registered_commands if command.name == "dx_qc")
    mock_callback = mocker.patch.object(command, "callback", autospec=True)

    result = runner.invoke(
        cli.cli,
        [
            "dx_qc",
            "HG002",
            "tests/data/dx_qc/HG002.wgs_coverage_metrics.csv",
            "tests/data/dx_qc/HG002.cnv_metrics.csv",
            "tests/data/dx_qc/HG002.mapping_metrics.csv",
            "tests/data/dx_qc/HG002.ploidy_estimation_metrics.csv",
            "tests/data/dx_qc/HG002.gvcf_metrics.csv",
        ],
    )

    assert result.exit_code == 0
    mock_callback.assert_called_once_with(
        sample_id="HG002",
        coverage_metrics_csv=Path("tests/data/dx_qc/HG002.wgs_coverage_metrics.csv"),
        cnv_metrics_csv=Path("tests/data/dx_qc/HG002.cnv_metrics.csv"),
        mapping_metrics_csv=Path("tests/data/dx_qc/HG002.mapping_metrics.csv"),
        ploidy_estimation_metrics_csv=Path("tests/data/dx_qc/HG002.ploidy_estimation_metrics.csv"),
        callability_metrics_csv=Path("tests/data/dx_qc/HG002.gvcf_metrics.csv"),
    )


def test_dx_qc_no_args(mocker: MockerFixture) -> None:
    """Test that the dx_qc command is registered and can be invoked."""
    command = next(command for command in dx_qc.cli.registered_commands if command.name == "dx_qc")
    mock_callback = mocker.patch.object(command, "callback", autospec=True)

    result = runner.invoke(cli.cli, ["dx_qc"])

    assert result.exit_code == 2
    mock_callback.assert_not_called()
