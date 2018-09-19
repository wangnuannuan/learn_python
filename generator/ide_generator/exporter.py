from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment
import os


class Exporter(object):
	TEMPLATE_DIR = os.path.abspath(join(dirname(__file__),'templates'))
	def __init__(self, toolchain):

		self.toolchain = toolchain

    def gen_file_raw(self, target_text, output, dest_path):
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        output = join(dest_path, output)
        logger.debug("Generating: %s" % output)

        open(output, "w").write(target_text)
        return dirname(output), output

    def gen_file_jinja(self, template_file, data, output, dest_path):
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        output = join(dest_path, output)
        logger.debug("Generating: %s" % output)

        """ Fills data to the project template, using jinja2. """
        env = Environment()
        template_file = os.path.join(self.TEMPLATE_DIR, self.toolchain)
        env.loader = FileSystemLoader(self.TEMPLATE_DIR)
        # TODO: undefined=StrictUndefined - this needs fixes in templates
        template = env.get_template(template_file)
        target_text = template.render(data)

        open(output, "w").write(target_text)
        return dirname(output), output