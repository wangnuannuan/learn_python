from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment
import os
from os.path import join, dirname, abspath, normpath, exists
import logging

logger = logging.getLogger('ide_generator.tools')
class Exporter(object):
    TEMPLATE_DIR = abspath(join(dirname(__file__),'templates'))
    def __init__(self, toolchain):

        self.toolchain = toolchain

    def gen_file_raw(self, target_text, output, dest_path):
        if not exists(dest_path):
            os.makedirs(dest_path)
        output = join(dest_path, output)
        logger.debug("Generating: %s" % output)

        open(output, "w").write(target_text)
        return dirname(output), output

    def gen_file_jinja(self, template_file, data, output, dest_path):
        if not exists(dest_path):
            os.makedirs(dest_path)
        output = join(dest_path, output)
        logger.debug("Generating: %s" % output)

        env = Environment()
        template_file_path = join(self.TEMPLATE_DIR, self.toolchain)
        env.loader = FileSystemLoader(template_file_path)
        template = env.get_template(template_file)
        target_text = template.render(data)

        open(output, "w").write(target_text)
        return dirname(output), output
