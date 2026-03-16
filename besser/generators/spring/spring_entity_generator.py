from collections import defaultdict
import os
import re
from typing import List
from jinja2 import Environment, FileSystemLoader
from besser.BUML.metamodel.structural import DomainModel
from besser.BUML.metamodel.structural.structural import BinaryAssociation, Class, Enumeration, Parameter, Property, StringType, BooleanType, DateTimeType, DateType, FloatType, IntegerType, TimeDeltaType, TimeType
from besser.generators import GeneratorInterface

class SpringEntityGenerator(GeneratorInterface):

    JAVA_TYPES = {
        StringType.name: "String",
        BooleanType.name: "Boolean",
        IntegerType.name: "Integer",
        FloatType.name: "Float",
        DateType.name: "LocalDate",
        DateTimeType.name: "LocalDateTime",
        TimeType.name: "LocalTime",
        TimeDeltaType.name: "Duration"
    }

    def __init__(self, model: DomainModel, 
                 output_dir: str = "./generated/entity", 
                 package_name: str = "com.example.entity"):
        super().__init__(model, output_dir)

        self.package_name: str = package_name
        self.enumerations: set[Enumeration] = model.get_enumerations()
        self.classes: List[Class] = model.classes_sorted_by_inheritance()
        self.relation_owners: dict[str, str] = self._get_relation_owner_map(model)

    def generate(self):
        model: DomainModel = self.model
        assoc_map: defaultdict[str, List[BinaryAssociation]] = defaultdict(list)

        for assoc in model.associations:
            end1, end2 = list(assoc.ends)
            assoc_map[end1.type.name].append(assoc)
            assoc_map[end2.type.name].append(assoc)

        for enum in self.enumerations:
            self._generate_enum_file(enum)
        
        for cls in self.classes:
            self._generate_class_file(cls, assoc_map[cls.name])

    def _generate_class_file(self, cls: Class, assocs_for_class: List[BinaryAssociation]):
        file_path = self.build_generation_path(file_name=f"{cls.name.capitalize()}.java")
        templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        env = Environment(loader=FileSystemLoader(templates_path))
        entity_template = env.get_template("entity.java.j2")

        relations: List[object] = self._prepare_relations(cls, assocs_for_class)

        imports: set[str] = self._get_default_imports().union(self._get_specific_imports_for_class(cls, relations))

        context = {
            "cls": cls,
            "package_name": self.package_name,
            "imports": sorted(list(imports)),
            "is_abstract": cls.is_abstract,
            "table_name": self._pluralize(cls.name.lower()),
            "parent": cls.parents().pop().name if cls.parents() else None,
            "attributes": sorted(
                            self._prepare_attributes(cls),
                            key=lambda a: (not a["is_id"], not a["is_enum"], not a["is_list"], a["name"])
                        ),
            "methods": self._prepare_methods(cls),
            "relations": self._prepare_relations(cls, assocs_for_class),
        }

        with open(file_path, mode="w", encoding="utf-8") as f:
            generated_code = entity_template.render(**context)
            f.write(generated_code)

    def _prepare_attributes(self, cls: Class) -> List[object]:
        attributes: List[object] = []

        for attr in cls.attributes:
            is_enum: bool = any(attr.type.name == enum.name for enum in self.enumerations)
            is_list: bool = attr.multiplicity.max != 1
            is_class: bool = any(attr.type.name == c.name for c in self.classes)
            attr_type = None

            if is_enum or is_class:
                attr_type = attr.type.name
            else:
                attr_type = self.JAVA_TYPES[attr.type.name]
            if is_list:
                attr_type = f"List<{attr_type}>"

            default_value: str = ""

            if attr.default_value:
                if attr.type.name == DateType.name:
                    default_value = f"""LocalDate.of{attr.default_value["year"], attr.default_value["month"], attr.default_value["day"]}"""
                elif attr.type.name == DateTimeType.name:
                    default_value = f"""LocalDateTime.of{attr.default_value["year"], attr.default_value["month"], attr.default_value["day"], attr.default_value["hour"], attr.default_value["minute"], attr.default_value["second"]}"""
                elif attr.type.name == TimeType.name:
                    default_value = f"""LocalTime.of{attr.default_value["hour"], attr.default_value["minute"], attr.default_value["second"]}"""
                elif attr.type.name == TimeDeltaType.name:
                    default_value = f"Duration.ofSeconds({attr.default_value})"
                elif attr.type.name == "str":
                    default_value = f"\"{attr.default_value}\""
                elif is_enum:
                    default_value = f"{attr.type.name}.{attr.default_value}"
                else:
                    default_value = attr.default_value

            attributes.append({
                "is_id": attr.is_id,
                "column_name": self._to_snake_case(attr.name),
                "is_optional": attr.is_optional,
                "is_enum": is_enum,
                "is_list": is_list,
                "visibility": attr.visibility,
                "type": attr_type,
                "name": attr.name,
                "default_value": default_value
            })
        
        return attributes
    
    def _prepare_methods(self, cls: Class) -> List[object]:
        methods: List[object] = []

        for method in cls.methods:
            method_return_type: str = ""

            if not method.type:
                method_return_type = "void"
            else:
                is_method_type_enum: bool = any(method.type.name == enum.name for enum in self.enumerations)
                is_method_type_class: bool = any(method.type.name == c.name for c in self.classes)

                if is_method_type_enum or is_method_type_class:
                    method_return_type = method.type.name
                else:
                    method_return_type = self.JAVA_TYPES[method.type.name]

            parameters: List[object] = []

            for parameter in method.parameters:
                is_enum: bool = any(parameter.type.name == enum.name for enum in self.enumerations)
                is_class: bool = any(parameter.type.name == c.name for c in self.classes)

                if is_enum or is_class:
                    param_type = parameter.type.name
                else:
                    param_type = self.JAVA_TYPES[parameter.type.name]

                parameters.append({
                    "name": parameter.name,
                    "type": param_type
                })
            
            methods.append({
                "name": method.name,
                "visibility": method.visibility,
                "return_type": method_return_type,
                "code": method.code,
                "parameters": parameters
            })

        return methods
    
    def _prepare_relations(self, cls: Class, assocs_for_class: List[BinaryAssociation]) -> List[object]:
        relations: List[object] = []

        for assoc in assocs_for_class:
            ends: List[Property] = list(assoc.ends)
            end1, end2 = ends

            if end1.type.name == cls.name and end2.is_navigable:
                source: Property = end1
                target: Property = end2
            elif end2.type.name == cls.name and end1.is_navigable:
                source: Property = end2
                target: Property = end1
            else:
                continue

            bidirectional: bool = source.is_navigable and target.is_navigable
            source_many = source.multiplicity.max != 1
            target_many = target.multiplicity.max != 1

            relation: str = None
            mapped_by: str = None
            owning: bool = True

            if not source_many and not target_many:
                relation = "OneToOne"
                if bidirectional and self.relation_owners[assoc.name] != source.type.name:
                    owning = False
                    mapped_by = source.name
            elif not source_many and target_many:
                relation = "OneToMany"
                if bidirectional:
                    owning = False
                    mapped_by = source.name
            elif source_many and not target_many:
                relation = "ManyToOne"
            elif source_many and target_many:
                relation = "ManyToMany"
                if bidirectional and self.relation_owners[assoc.name] != source.type.name:
                    owning = False
                    mapped_by = source.name
            
            relations.append({
                "assoc": assoc.name,
                "source_property": source.name,
                "target_property": target.name,
                "source_cls": source.type.name,
                "target_cls": target.type.name,
                "relation": relation,
                "mapped_by": mapped_by,
                "join_column": f"{self._to_snake_case(target.type.name)}_id",
                "owning": owning,
                "is_list": target_many,
                "type": f"List<{target.type.name}>" if target_many else target.type.name,
                "to_snake_case": self._to_snake_case
            })

        return relations
    
    def _get_relation_owner_map(self, model: DomainModel) -> dict[str, str]:
        ret: dict[str, str] = {}

        for assoc in model.associations:
            end1, end2 = list(assoc.ends)
            if (end1.multiplicity != 1 and end2.multiplicity != 1) or (end1.multiplicity == 1 and end2.multiplicity == 1) and end1.is_navigable and end2.is_navigable:
                ret[assoc.name] = end1.type.name

        return ret

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

    def _get_default_imports(self) -> set[str]:
        return set([
            "jakarta.persistence.Entity",
            "jakarta.persistence.Table",
            "jakarta.persistence.Id",
            "jakarta.persistence.GeneratedValue",
            "jakarta.persistence.GenerationType",
            "jakarta.persistence.Column",
        ])
    
    def _get_specific_imports_for_class(self, cls: Class, relations: List[object]) -> set[str]:
        imports: set[str] = set()

        if cls.is_abstract:
            imports.add("jakarta.persistence.MappedSuperclass")

        if any(any(attr.type.name == enum.name for enum in self.enumerations) for attr in cls.attributes):
            imports.add("jakarta.persistence.Enumerated")
            imports.add("jakarta.persistence.EnumType")

        for attr in cls.attributes:
            if attr.type.name == DateType.name:
                imports.add("java.time.LocalDate")
            elif attr.type.name == DateTimeType.name:
                imports.add("java.time.LocalDateTime")
            elif attr.type.name == TimeType.name:
                imports.add("java.time.LocalTime")
            elif attr.type.name == TimeDeltaType.name:
                imports.add("java.time.Duration")

            if attr.multiplicity.max != 1:
                imports.add("java.util.List")
                imports.add("java.util.ArrayList")
                if attr.default_value:
                    imports.add("java.util.Arrays")

        for method in cls.methods:
            if method.type:
                if method.type.name == DateType.name:
                    imports.add("java.time.LocalDate")
                elif method.type.name == DateTimeType.name:
                    imports.add("java.time.LocalDateTime")
                elif method.type.name == TimeType.name:
                    imports.add("java.time.LocalTime")
                elif method.type.name == TimeDeltaType.name:
                    imports.add("java.time.Duration")

            for parameter in method.parameters:
                if parameter.type.name == DateType.name:
                    imports.add("java.time.LocalDate")
                elif parameter.type.name == DateTimeType.name:
                    imports.add("java.time.LocalDateTime")
                elif parameter.type.name == TimeType.name:
                    imports.add("java.time.LocalTime")
                elif parameter.type.name == TimeDeltaType.name:
                    imports.add("java.time.Duration")

        for relation in relations:
            if relation["is_list"]:
                imports.add("java.util.List")
                imports.add("java.util.ArrayList")
                imports.add("java.util.Arrays")
            if relation["relation"] == "OneToOne":
                imports.add("jakarta.persistence.OneToOne")
                if relation["owning"]:
                    imports.add("jakarta.persistence.JoinColumn")
            if relation["relation"] == "OneToMany":
                imports.add("jakarta.persistence.OneToMany")
                if relation["owning"]:
                    imports.add("jakarta.persistence.JoinColumn")
            if relation["relation"] == "ManyToOne":
                imports.add("jakarta.persistence.ManyToOne")
                imports.add("jakarta.persistence.JoinColumn")
            if relation["relation"] == "ManyToMany":
                imports.add("jakarta.persistence.ManyToMany")
                if relation["owning"]:
                    imports.add("jakarta.persistence.JoinTable")
                    imports.add("jakarta.persistence.JoinColumn")

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
