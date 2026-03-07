import os
from typing import List
from jinja2 import Environment, FileSystemLoader
from besser.BUML.metamodel.structural import DomainModel
from besser.BUML.metamodel.structural.structural import Class
from besser.generators import GeneratorInterface
from besser.utilities.utils import sort_by_timestamp


class SpringEntityGenerator(GeneratorInterface):

    def __init__(self, model: DomainModel, 
                 output_dir: str = "./generated/entities", 
                 package_name: str = "com.example.entities"):
        super().__init__(model, output_dir)

        self.package_name: str = package_name

    def generate(self):
        model: DomainModel = self.model
        
        for cls in model.classes_sorted_by_inheritance():
            self._generate_class_file(cls)
        

    def _generate_class_file(self, cls: Class):
        file_path = self.build_generation_path(file_name=f"{cls.name.capitalize()}.java")
        templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        env = Environment(loader=FileSystemLoader(templates_path))
        entity_template = env.get_template("entity.j2")

        imports: List[str] = self._get_default_imports()

        if cls.is_abstract:
            imports.append("javax.persistence.MappedSuperclass")

        context = {
            "cls": cls,
            "package_name": self.package_name,
            "imports": imports,
            "is_abstract": cls.is_abstract,
            "table_name": self._pluralize(cls.name.lower()),
            "parent": cls.parents().pop().name if cls.parents() else None
        }
        
        with open(file_path, mode="w", encoding="utf-8") as f:
            generated_code = entity_template.render(**context)
            f.write(generated_code)

    def _get_default_imports(self) -> List[str]:
        return [
            "jakarta.persistence.Entity",
            "jakarta.persistence.Table",
            "jakarta.persistence.Id",
        ]
    
    @staticmethod
    def _pluralize(name: str) -> str:
        if name.endswith("y"):
            return name[:-1] + "ies"
        elif name.endswith(("s", "x", "z", "ch", "sh")):
            return name + "es"
        else:
            return name + "s"
