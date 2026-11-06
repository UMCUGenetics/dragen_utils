import jinja2
import typer

cli = typer.Typer()


def render_igv_session(samplename: str) -> None:
    """Render IGV session XML with samplename as placeholder variable.

    Args:
        samplename: Samplename used to fill the template placeholders.

    """
    jinja_env = jinja2.Environment(
        loader=jinja2.PackageLoader("dragen_utils", "templates"),
    )
    xml_template_name = "IGV_srWGS_SampleQC_session.xml"
    template = jinja_env.get_template(xml_template_name)
    rendered_template = template.render(sample=samplename)
    with open(f"{samplename}_{xml_template_name}", "w") as xml_handle:
        xml_handle.write(rendered_template)


@cli.command("igv_session")
def main(samplename: str) -> None:
    """Render an IGV session XML file for a sample by filling in the sample name in the Jinja session template.

    Args:
        samplename: Sample name used to fill the template placeholders.
    """
    render_igv_session(samplename=samplename)


if __name__ == "__main__":
    main()
