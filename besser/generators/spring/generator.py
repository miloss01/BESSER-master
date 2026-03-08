import os
import re
from typing import List
from jinja2 import Environment, FileSystemLoader
from besser.BUML.metamodel.structural import DomainModel
from besser.BUML.metamodel.structural.structural import Class, Enumeration, StringType, BooleanType, DateTimeType, DateType, FloatType, IntegerType, TimeDeltaType, TimeType
from besser.generators import GeneratorInterface

class SpringEntityGenerator(GeneratorInterface):

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
                 output_dir: str = "./generated/entities", 
                 package_name: str = "com.example.entities"):
        super().__init__(model, output_dir)

        self.package_name: str = package_name
        self.enumerations: set[Enumeration] = model.get_enumerations()

    def generate(self):
        model: DomainModel = self.model

        for enum in model.get_enumerations():
            self._generate_enum_file(enum)
        
        for cls in model.classes_sorted_by_inheritance():
            self._generate_class_file(cls)

    def _generate_class_file(self, cls: Class):
        file_path = self.build_generation_path(file_name=f"{cls.name.capitalize()}.java")
        templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        env = Environment(loader=FileSystemLoader(templates_path))
        entity_template = env.get_template("entity.j2")

        imports: List[str] = self._get_default_imports() + self._get_specific_imports_for_class(cls)

        attributes: List[object] = []

        for attr in cls.attributes:
            is_enum: bool = any(attr.type.name == enum.name for enum in self.enumerations)

            attributes.append({
                "is_id": attr.is_id,
                "column_name": self._to_snake_case(attr.name),
                "is_optional": attr.is_optional,
                "is_enum": is_enum,
                "visibility": attr.visibility,
                "type": self.JAVA_TYPES[attr.type.name] if not is_enum else attr.type.name,
                "name": attr.name,
                "default_value": f"\"{attr.default_value}\"" if attr.default_value and attr.type.name == "str" else attr.default_value
            })

        context = {
            "cls": cls,
            "package_name": self.package_name,
            "imports": imports,
            "is_abstract": cls.is_abstract,
            "table_name": self._pluralize(cls.name.lower()),
            "parent": cls.parents().pop().name if cls.parents() else None,
            "attributes": sorted(
                            attributes,
                            key=lambda a: (not a["is_id"], not a["is_enum"], a["name"])
                        )
        }
        
        with open(file_path, mode="w", encoding="utf-8") as f:
            generated_code = entity_template.render(**context)
            f.write(generated_code)

    def _generate_enum_file(self, enum: Enumeration):
        file_path = self.build_generation_path(file_name=f"{enum.name.capitalize()}.java")
        templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        env = Environment(loader=FileSystemLoader(templates_path))
        entity_template = env.get_template("enum.java.j2")

        context = {
            "package_name": self.package_name,
            "name": enum.name.capitalize(),
            "literals": enum.literals
        }

        with open(file_path, mode="w", encoding="utf-8") as f:
            generated_code = entity_template.render(**context)
            f.write(generated_code)

    def _get_default_imports(self) -> List[str]:
        return [
            "jakarta.persistence.Entity",
            "jakarta.persistence.Table",
            "jakarta.persistence.Id",
            "jakarta.persistence.GeneratedValue",
            "jakarta.persistence.Column",
        ]
    
    def _get_specific_imports_for_class(self, cls: Class) -> List[str]:
        imports: List[str] = []

        if cls.is_abstract:
            imports.append("javax.persistence.MappedSuperclass")

        if any(any(attr.type.name == enum.name for enum in self.enumerations) for attr in cls.attributes):
            imports.append("jakarta.persistence.Enumerated")

        for attr in cls.attributes:
            if attr.type.name == DateType.name:
                imports.append("java.time.LocalDate")
            elif attr.type.name in [DateTimeType.name, TimeType.name]:
                imports.append("java.time.LocalDateTime")
            elif attr.type.name == TimeDeltaType.name:
                imports.append("java.time.Duration")

        return imports
    
    @staticmethod
    def _pluralize(name: str) -> str:
        if name.endswith("y"):
            return name[:-1] + "ies"
        elif name.endswith(("s", "x", "z", "ch", "sh")):
            return name + "es"
        else:
            return name + "s"
        
    @staticmethod
    def _to_snake_case(name: str) -> str:
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
