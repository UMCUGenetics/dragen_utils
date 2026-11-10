from pathlib import Path

import jinja2
import typer

cli = typer.Typer()


def render_igv_session(sample_id: str, bam: Path, tn_bw: Path, filtered_baf_bw: Path) -> None:
    """Render IGV session XML sample files as placeholder.

    Args:
        sample_id: Sample name. Used for output filename. Sample_1
        bam: Sample bam file. Sample_1_flowcell.bam
        tn_bw: Sample tn_nw Sample_1_flowcell.tn.bw
        filtered_baf_bw: Sample hard filtered baf file. Sample_1_flowcell.hard_filtered.baf.bw

    """
    jinja_env = jinja2.Environment(
        loader=jinja2.PackageLoader("dragen_utils", "templates"),
    )
    xml_template_name = "IGV_srWGS_SampleQC_session.xml"
    template = jinja_env.get_template(xml_template_name)
    # remove full path to allow XML file to be copied to other location.
    template_data = {"bam": bam.name, "tn_bw": tn_bw.name, "filtered_baf_bw": filtered_baf_bw.name}
    rendered_template = template.render(template_data=template_data)
    xml_path_out = Path(f"{sample_id}_{xml_template_name}")
    xml_path_out.open("w", encoding="utf-8").write(rendered_template)


@cli.command("igv_session")
def main(sample_id: str, bam: Path, tn_bw: Path, filtered_baf_bw: Path) -> None:
    """Render an IGV session XML file for a sample by adding selected files to XML template with Jinja2.

    Args:
        sample_id: Sample name. Used for output filename. Sample_1
        bam: Sample bam file. Sample_1_flowcell.bam
        tn_bw: Sample tn_nw Sample_1_flowcell.tn.bw
        filtered_baf_bw: Sample hard filtered baf file. Sample_1_flowcell.hard_filtered.baf.bw

    Raises:
        typer.BadParameter: Incorrect file extension is provided.

    """
    # Check if correct files are provided for template.
    for file, suffix in ((bam, ".bam"), (tn_bw, ".tn.bw"), (filtered_baf_bw, ".baf.bw")):
        if not file.name.endswith(suffix):
            raise typer.BadParameter(f"Expected a '{suffix}' file, got: '{file.name}'")

    render_igv_session(sample_id=sample_id, bam=bam, tn_bw=tn_bw, filtered_baf_bw=filtered_baf_bw)


if __name__ == "__main__":
    main()
