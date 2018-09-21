from ide_generator.project import Ide
from ide_generator.generate import Generator
generator = Generator("projects.yaml")
#generator = Ide("baremetal_arc_feature_cache","projects.yaml")
for project in generator.generate("baremetal_arc_feature_cache"):
    project.generate("test")

