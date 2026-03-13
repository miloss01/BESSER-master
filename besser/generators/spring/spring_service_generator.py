import os
from pathlib import Path
from typing import List

from jinja2 import Environment, FileSystemLoader

from besser.BUML.metamodel.structural.structural import BooleanType, Class, DateTimeType, DateType, DomainModel, Enumeration, FloatType, IntegerType, StringType, TimeDeltaType, TimeType
from besser.generators.generator_interface import GeneratorInterface

class SpringServiceGenerator(GeneratorInterface):

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
                 repository_package_name: str,
                 output_dir: str = "./generated/service", 
                 package_name: str = "com.example.service"):
        super().__init__(model, output_dir)

        self.package_name: str = package_name
        self.entity_package_name: str = entity_package_name
        self.repository_package_name: str = repository_package_name
        self.enumerations: set[Enumeration] = model.get_enumerations()
        self.classes: set[Class] = model.classes_sorted_by_inheritance()

    def generate(self):
        for cls in self.classes:
            if not cls.is_abstract: 
                self._generate_service_files(cls)

    def _generate_service_files(self, cls: Class):
        templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        env = Environment(loader=FileSystemLoader(templates_path), trim_blocks=True)

        file_path = self.build_generation_path(file_name=Path("interfaces") / f"I{cls.name.capitalize()}Service.java")
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        iservice_template = env.get_template("iservice.java.j2")

        imports: set[str] = set()
        imports.add(f"{self.entity_package_name}.{cls.name}")
        imports.add("java.util.List")

        if cls.attributes:
            imports.add("java.util.ArrayList")
            imports.add("java.util.Optional")

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

        methods.extend(self._get_crud_methods(cls))

        context = {
            "package": f"{self.package_name}.interfaces",
            "imports": sorted(imports),
            "cls": cls.name,
            "methods": sorted(methods, key=lambda m: m["name"])
        }

        with open(file_path, mode="w", encoding="utf-8") as f:
            generated_code = iservice_template.render(**context)
            f.write(generated_code)

        file_path = self.build_generation_path(file_name=Path("impl") / f"{cls.name.capitalize()}Service.java")
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        service_template = env.get_template("service.java.j2")

        context["package"] = f"{self.package_name}.impl"

        imports.add("org.springframework.beans.factory.annotation.Autowired")
        imports.add("org.springframework.stereotype.Service")
        imports.add(f"{self.package_name}.interfaces.I{cls.name.capitalize()}Service")
        imports.add(f"{self.repository_package_name}.I{cls.name.capitalize()}Repository")

        context["imports"] = sorted(imports)

        for method in context["methods"]:
            parameter: str = method["parameter"]
            tokens: List[str] = parameter.split(", ")
            method["parameter_names"] = ", ".join(token.split(" ")[1] for token in tokens) if parameter else ""

        with open(file_path, mode="w", encoding="utf-8") as f:
            generated_code = service_template.render(**context)
            f.write(generated_code)

    def _get_crud_methods(self, cls: Class) -> List[object]:
        return [
            {
                "return_value": f"List<{cls.name}>",
                "name": "findAll",
                "parameter": ""
            },
            {
                "return_value": f"Optional<{cls.name}>",
                "name": "findById",
                "parameter": "Integer id"
            },
            {
                "return_value": f"{cls.name}",
                "name": "save",
                "parameter": f"{cls.name} {cls.name[0].lower() + cls.name[1:]}"
            },
            {
                "return_value": "void",
                "name": "delete",
                "parameter": f"{cls.name} {cls.name[0].lower() + cls.name[1:]}"
            }
        ]
