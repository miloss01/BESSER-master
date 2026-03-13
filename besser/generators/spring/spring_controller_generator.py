import os
from pathlib import Path
from typing import List

from jinja2 import Environment, FileSystemLoader

from besser.BUML.metamodel.structural.structural import BooleanType, Class, DateTimeType, DateType, DomainModel, Enumeration, FloatType, IntegerType, StringType, TimeDeltaType, TimeType
from besser.generators.generator_interface import GeneratorInterface

class SpringControllerGenerator(GeneratorInterface):

    def __init__(self, model: DomainModel, 
                 entity_package_name: str,
                 service_package_name: str,
                 output_dir: str = "./generated/controller", 
                 package_name: str = "com.example.controller"):
        super().__init__(model, output_dir)

        self.package_name: str = package_name
        self.entity_package_name: str = entity_package_name
        self.service_package_name: str = service_package_name
        self.enumerations: set[Enumeration] = model.get_enumerations()
        self.classes: set[Class] = model.classes_sorted_by_inheritance()

    def generate(self):
        for cls in self.classes:
            if not cls.is_abstract: 
                self._generate_controller_file(cls)

    def _generate_controller_file(self, cls: Class):
        file_path = self.build_generation_path(file_name=f"{cls.name.capitalize()}Controller.java")
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        env = Environment(loader=FileSystemLoader(templates_path), trim_blocks=True)
        repository_template = env.get_template("controller.java.j2")

        imports: set[str] = set()
        imports.add("org.springframework.beans.factory.annotation.Autowired")
        imports.add("org.springframework.web.bind.annotation.RestController")
        imports.add("org.springframework.web.bind.annotation.RequestMapping")
        imports.add("org.springframework.web.bind.annotation.PathVariable")
        imports.add("org.springframework.web.bind.annotation.RequestBody")
        imports.add("org.springframework.web.bind.annotation.GetMapping")
        imports.add("org.springframework.web.bind.annotation.PostMapping")
        imports.add("org.springframework.web.bind.annotation.PutMapping")
        imports.add("org.springframework.web.bind.annotation.DeleteMapping")
        imports.add("org.springframework.http.ResponseEntity")
        imports.add("java.util.Optional")
        imports.add("java.util.List")
        imports.add(f"{self.service_package_name}.interfaces.I{cls.name.capitalize()}Service")
        imports.add(f"{self.entity_package_name}.{cls.name}")

        context = {
            "package": f"{self.package_name}",
            "imports": sorted(imports),
            "cls": cls.name
        }

        with open(file_path, mode="w", encoding="utf-8") as f:
            generated_code = repository_template.render(**context)
            f.write(generated_code)
