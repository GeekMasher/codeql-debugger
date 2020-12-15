import os
import jinja2
import logging

TEMPLATES = os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")


def render(metadata, output):

    logging.info("Loading templates from :: " + TEMPLATES)

    templateLoader = jinja2.FileSystemLoader(searchpath=TEMPLATES)
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "report.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(**metadata)

    with open(output, "w") as handle:
        handle.write(outputText)
