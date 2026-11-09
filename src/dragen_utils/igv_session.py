from pathlib import Path

import jinja2
import typer

cli = typer.Typer()


def render_igv_session(bam: Path, tn_bw: Path, filtered_baf_bw: Path) -> None:
    """Render IGV session XML sample files as placeholder.

    Args:
        bam: Sample bam file. Sample_1_flowcell.bam
        tn_bw: Sample tn_nw Sample_1_flowcell.tn.bw
        filtered_baf_bw: Sample hard filtered baf file. Sample_1_flowcell.hard_filtered.baf.bw
    """
    jinja_env = jinja2.Environment(
        loader=jinja2.PackageLoader("dragen_utils", "templates"),
    )
    xml_template_name = "IGV_srWGS_SampleQC_session.xml"
    template = jinja_env.get_template(xml_template_name)
    samplename = bam.stem
    template_data = {"bam": bam, "tn_bw": tn_bw, "filtered_baf_bw": filtered_baf_bw}
    rendered_template = template.render(template_data=template_data)
    with open(f"{samplename}_{xml_template_name}", "w") as xml_handle:
        xml_handle.write(rendered_template)


@cli.command("igv_session")
def main(bam: Path, tn_bw: Path, filtered_baf_bw: Path) -> None:
    """Render an IGV session XML file for a sample by adding selected files to XML template with Jinja2.
    Args:
        bam: Sample bam file. Sample_1_flowcell.bam
        tn_bw: Sample tn_nw Sample_1_flowcell.tn.bw
        filtered_baf_bw: Sample hard filtered baf file. Sample_1_flowcell.hard_filtered.baf.bw
    """
    # TODO: Check if file extensions are correct.
    # TODO: Samplename
    # TODO: Get correct filename. It could be a nested item or symbolic link.
    render_igv_session(bam=bam, tn_bw=tn_bw, filtered_baf_bw=filtered_baf_bw)


if __name__ == "__main__":
    main()
