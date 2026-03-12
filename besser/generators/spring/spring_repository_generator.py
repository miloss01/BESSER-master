import os
from pathlib import Path
from typing import List

from jinja2 import Environment, FileSystemLoader

from besser.BUML.metamodel.structural.structural import BooleanType, Class, DateTimeType, DateType, DomainModel, Enumeration, FloatType, IntegerType, StringType, TimeDeltaType, TimeType
from besser.generators.generator_interface import GeneratorInterface

class SpringRepositoryGenerator(GeneratorInterface):

    JAVA_TYPES = {
        StringType.name: "String",
        BooleanType.name: "Boolean",
        IntegerType.name: "Integer",
        FloatType.name: "Float",
        DateType.name: "LocalDate",
        DateTimeType.name: "LocalDateTime",
        TimeType.name: "LocalDateTime",
        TimeDeltaType.name: "Duration"
    }

    def __init__(self, model: DomainModel, 
                 entity_package_name: str,
                 output_dir: str = "./generated/repository", 
                 package_name: str = "com.example.repository"):
        super().__init__(model, output_dir)

        self.package_name: str = package_name
        self.entity_package_name: str = entity_package_name
        self.enumerations: set[Enumeration] = model.get_enumerations()
        self.classes: set[Class] = model.classes_sorted_by_inheritance()

    def generate(self):
        model: DomainModel = self.model

        for cls in self.classes:
            if not cls.is_abstract: 
                self._generate_repository_file(cls)

    def _generate_repository_file(self, cls: Class):
        file_path = self.build_generation_path(file_name=f"I{cls.name.capitalize()}Repository.java")
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        env = Environment(loader=FileSystemLoader(templates_path), trim_blocks=True)
        repository_template = env.get_template("irepository.java.j2")

        imports: set[str] = set()
        imports.add("org.springframework.data.jpa.repository.JpaRepository")
        imports.add(f"{self.entity_package_name}.{cls.name}")

        if cls.attributes:
            imports.add("java.util.ArrayList")

        methods: List[object] = []
        
        for attr in cls.attributes:
            is_enum: bool = any(attr.type.name == enum.name for enum in self.enumerations)
            is_list: bool = attr.multiplicity.max != 1
            is_class: bool = any(attr.type.name == c.name for c in self.classes)

            if is_list or attr.is_id:
                continue

            method: object = {}

            method["return_value"] = f"ArrayList<{cls.name}>"
            method["name"] = f"findAllBy{attr.name.capitalize()}"

            if is_enum or is_class:
                parameter_type = attr.type.name
                imports.add(f"{self.entity_package_name}.{attr.type.name}")
            else:
                parameter_type = self.JAVA_TYPES[attr.type.name]

            method["parameter"] = f"{parameter_type} {attr.name}"

            if attr.type.name == DateType.name:
                imports.add("java.time.LocalDate")
            elif attr.type.name in [DateTimeType.name, TimeType.name]:
                imports.add("java.time.LocalDateTime")
            elif attr.type.name == TimeDeltaType.name:
                imports.add("java.time.Duration")

            if attr.type.name in [DateType.name, DateTimeType.name, TimeType.name]:
                methods.append({
                    "return_value": f"ArrayList<{cls.name}>",
                    "name": f"findAllBy{attr.name.capitalize()}Between",
                    "parameter": f"{parameter_type} start, {parameter_type} end"
                })

            methods.append(method)

        context = {
            "package": f"{self.package_name}",
            "imports": sorted(imports),
            "cls": cls.name,
            "methods": sorted(methods, key=lambda m: m["name"])
        }

        with open(file_path, mode="w", encoding="utf-8") as f:
            generated_code = repository_template.render(**context)
            f.write(generated_code)
