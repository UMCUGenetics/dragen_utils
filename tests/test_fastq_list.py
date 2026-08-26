from pathlib import Path

from dragen_utils.fastq_list import get_fastq_metadata, get_rg_id, get_rg_lb, main


def test_get_fastq_metadata():
    fastq_file = Path("tests/data/fastq_list/HG002-1_23KCWCLT3_S8_L004_R1_001.fastq.gz")

    expected_metadata = {
        "sample_id": "HG002-1",
        "machine": "@LH00927",
        "run": "132",
        "flowcell": "23KCWCLT3",
        "lane": "4",
    }
    actual_metadata = get_fastq_metadata(fastq_file)

    assert actual_metadata == expected_metadata


def test_get_rg_id():
    fastq_metadata = {
        "sample_id": "HG002-1",
        "machine": "@LH00927",
        "run": "132",
        "flowcell": "23KCWCLT3",
        "lane": "4",
    }

    rg_id = get_rg_id(fastq_metadata)

    assert rg_id == "HG002-1_23KCWCLT3_4"


def test_get_rg_lb():
    fastq_metadata = {
        "sample_id": "HG002-1",
        "machine": "@LH00927",
        "run": "132",
        "flowcell": "23KCWCLT3",
        "lane": "4",
    }

    rg_lb = get_rg_lb(fastq_metadata)

    assert rg_lb == "HG002-1_23KCWCLT3"


def test_main(capsys):
    main(directory=Path("tests/data/fastq_list/"))

    captured = capsys.readouterr()
    assert "RGSM,RGID,RGLB,RGPL,Lane,Read1File,Read2File" in captured.out
    assert (
        "HG002-1,HG002-1_23KCWCLT3_4,HG002-1_23KCWCLT3,ILLUMINA,4,HG002-1_23KCWCLT3_S8_L004_R1_001.fastq.gz,HG002-1_23KCWCLT3_S8_L004_R2_001.fastq.gz"
        in captured.out
    )
    assert (
        "HG002-2,HG002-2_23KCWCLT3_4,HG002-2_23KCWCLT3,ILLUMINA,4,HG002-2_23KCWCLT3_S14_L004_R1_001.fastq.gz,HG002-2_23KCWCLT3_S14_L004_R2_001.fastq.gz"
        in captured.out
    )
