from pathlib import Path

import pytest
import typer
from pytest_mock import MockerFixture
from typer.testing import CliRunner

from dragen_utils import cli
from dragen_utils.igv_session import main, render_igv_session

runner = CliRunner()


def test_render_igv_session(tmp_path: Path, monkeypatch):
    """Test if output file is rendered correctly with filenames in content."""
    monkeypatch.chdir(tmp_path)
    sample_id = "HG002"
    # Function requires path objects, they do not need to exist.
    bam = tmp_path / "HG002.bam"
    tn_bw = tmp_path / "HG002.tn.bw"
    filtered_baf_bw = tmp_path / "HG002.hard-filtered.baf.bw"

    render_igv_session(sample_id=sample_id, bam=bam, tn_bw=tn_bw, filtered_baf_bw=filtered_baf_bw)

    output = tmp_path / "HG002_IGV_srWGS_SampleQC_session.xml"
    assert output.exists()
    content = output.read_text(encoding="utf-8")
    assert content.startswith('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
    assert '<Resource path="HG002.bam" type="bam"/>' in content
    assert '<Resource path="HG002.tn.bw" type="bw"/>' in content
    assert '<Resource path="HG002.hard-filtered.baf.bw" type="bw"/>' in content
    assert "{{" not in content


@pytest.mark.parametrize(
    ("bam", "tn_bw", "filtered_baf_bw", "match"),
    [
        ("HG002.txt", "HG002.tn.bw", "HG002.baf.bw", r"Expected a '\.bam' file"),
        ("HG002.bam", "HG002.bw", "HG002.baf.bw", r"Expected a '\.tn\.bw' file"),
        ("HG002.bam", "HG002.tn.bw", "HG002.baf.txt", r"Expected a '\.baf\.bw' file"),
    ],
)
def test_main_wrong_suffix(bam: str, tn_bw: str, filtered_baf_bw: str, match: str):
    """Test the three different errors that are raised if an incorrect suffix is given."""
    with pytest.raises(typer.BadParameter, match=match):
        main(sample_id="HG002", bam=Path(bam), tn_bw=Path(tn_bw), filtered_baf_bw=Path(filtered_baf_bw))


def test_main_name_validation_only(mocker: MockerFixture):
    """Test if main does not Raises an exception if all file extensions are correct."""
    mock_render = mocker.patch("dragen_utils.igv_session.render_igv_session")

    result = runner.invoke(cli.cli, ["igv_session", "HG002", "HG002.bam", "HG002.tn.bw", "HG002.hard-filtered.baf.bw"])

    assert result.exit_code == 0
    mock_render.assert_called_once_with(
        sample_id="HG002",
        bam=Path("HG002.bam"),
        tn_bw=Path("HG002.tn.bw"),
        filtered_baf_bw=Path("HG002.hard-filtered.baf.bw"),
    )
