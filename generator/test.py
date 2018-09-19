from ide_generator.project import Ide
from ide_generator.generate import Generator
generator = Generator("projects.yaml")
#generator = Ide("baremetal_arc_feature_cache","projects.yaml")
generator.generate("baremetal_arc_feature_cache")
