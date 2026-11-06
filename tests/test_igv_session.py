from dragen_utils.igv_session import render_igv_session


def test_render_igv_session(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    render_igv_session(samplename="testsample")
    with open("testsample_IGV_srWGS_SampleQC_session.xml") as handle:
        igv_session = handle.read()
    assert "{{ sample }}" not in igv_session
    assert "testsample.hard-filtered.baf.bw" in igv_session
