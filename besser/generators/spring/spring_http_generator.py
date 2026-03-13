import os
from pathlib import Path
from typing import List

from jinja2 import Environment, FileSystemLoader

from besser.BUML.metamodel.structural.structural import BooleanType, Class, DateTimeType, DateType, DomainModel, Enumeration, FloatType, IntegerType, StringType, TimeDeltaType, TimeType
from besser.generators.generator_interface import GeneratorInterface

class SpringHttpGenerator(GeneratorInterface):

    def __init__(self, model: DomainModel,
                 output_dir: str = "./generated/http"):
        super().__init__(model, output_dir)

        self.enumerations: set[Enumeration] = model.get_enumerations()
        self.classes: set[Class] = model.classes_sorted_by_inheritance()

    def generate(self):
        for cls in self.classes:
            if not cls.is_abstract: 
                self._generate_http_file(cls)
    
    def _generate_http_file(self, cls: Class):
        file_path = self.build_generation_path(file_name=f"{cls.name[0].lower() + cls.name[1:]}.http")
        templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        env = Environment(loader=FileSystemLoader(templates_path), trim_blocks=True)
        http_template = env.get_template("http.http.j2")

        context = {
            "cls": cls.name
        }

        with open(file_path, mode="w", encoding="utf-8") as f:
            generated_code = http_template.render(**context)
            f.write(generated_code)
