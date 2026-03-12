"""
Spring Entity Code Generator for BESSER B-UML Models
Generates Spring JPA Entity classes from BESSER structural models
With full support for JPA/Hibernate associations and BESSER metamodel features

BESSER dokumentacija:
https://besser.readthedocs.io/en/latest/api/BUML/metamodel/api_structural.html

Features:
- Apstraktne klase (abstract classes)
- Enumeracije (enumerations)
- ID atributi (@Id annotation)
- Navigable fields
- Opcioni atributi
- Visibility modifiers (public, private, protected)
- Readonly atributi (@Immutable)
- Izvedeni atributi (derived)
- Updatable/Insertable constraints
- Opisi (descriptions) i metadata
- Unique constraints
- Inheritance strategies

Author: Generator for BESSER-PEARL/BESSER
"""

from typing import Set, Dict, List, Optional
from pathlib import Path
import re
from enum import Enum
from jinja2 import Template, Environment, FileSystemLoader

from besser.BUML.metamodel.structural.structural import (
    Class, Association, DomainModel, Property, Type, Multiplicity, Enumeration
)
from besser.generators.generator_interface import GeneratorInterface


class SpringEntityGenerator(GeneratorInterface):
    """
    Generator za Spring Entity klase iz BESSER B-UML modela.
    
    Podržava sve BESSER metamodel koncepte:
    - Apstraktne klase
    - Enumeracije
    - ID atributi
    - Navigable polja
    - Opcioni atributi
    - Visibility modifiers
    - Readonly atributi
    - Izvedeni atributi
    - Updatable/Insertable constraints
    - Inheritance
    - Sva JPA/Hibernate asocijacije
    
    Primer korišćenja:
    ```python
    from besser.BUML.metamodel.structural.structural import Diagram
    from spring_entity_generator import SpringEntityGenerator
    
    diagram = Diagram()
    # ... dodaj klase, atribute, relacije ...
    
    generator = SpringEntityGenerator(
        diagram, 
        output_path="./src/main/java",
        templates_path="./templates"
    )
    generator.generate()
    ```
    """
    
    # Java tipovi mapiranje
    JAVA_TYPE_MAPPING = {
        'String': 'String',
        'Integer': 'Integer',
        'Int': 'Integer',
        'Long': 'Long',
        'Double': 'Double',
        'Float': 'Float',
        'Boolean': 'Boolean',
        'Bool': 'Boolean',
        'LocalDate': 'LocalDate',
        'LocalDateTime': 'LocalDateTime',
        'Date': 'LocalDateTime',
        'BigDecimal': 'BigDecimal',
        'UUID': 'UUID',
    }
    
    def __init__(self, model, output_path: str = "./generated/entities", 
                 package_name: str = "com.example.entity",
                 templates_path: str = "./templates"):
        """
        Inicijalizuj generator
        
        Args:
            model: B-UML Diagram model
            output_path: Putanja gde će biti sačuvane generirane klase
            package_name: Java package za generirane klase
            templates_path: Putanja do Jinja2 template fajlova
        """
        super().__init__(model)
        self.output_path = Path(output_path)
        self.package_name = package_name
        self.templates_path = Path(templates_path)
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # Inicijalizuj Jinja2 okruženje
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_path)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Mapiranje B-UML klasa sa njihovim asocijacijama
        self.associations_by_class: Dict[str, List[Association]] = {}
        self.enumerations: Dict[str, Enumeration] = {}
        
        self._build_association_map()
        self._build_enumerations_map()
    
    def _build_association_map(self):
        """Gradi mapu asocijacija za svaku klasu"""
        if not hasattr(self.model, 'classes') or self.model.classes is None:
            return
        
        for cls in self.model.classes:
            self.associations_by_class[cls.name] = []
        
        for cls in self.model.classes:
            if hasattr(cls, 'association_ends') and cls.association_ends:
                for assoc_end in cls.association_ends:
                    if hasattr(assoc_end, 'association'):
                        assoc = assoc_end.association
                        if assoc not in self.associations_by_class[cls.name]:
                            self.associations_by_class[cls.name].append(assoc)
    
    def _build_enumerations_map(self):
        """Gradi mapu enumeracija"""
        if not hasattr(self.model, 'enumerations') or self.model.enumerations is None:
            return
        
        for enum in self.model.enumerations:
            self.enumerations[enum.name] = enum
    
    def generate(self) -> List[str]:
        """
        Generiši sve Spring Entity klase i enumeracije
        
        Returns:
            Lista putanja generianih datoteka
        """
        generated_files = []
        
        # Generiši enumeracije
        if hasattr(self.model, 'enumerations') and self.model.enumerations:
            for enum in self.model.enumerations:
                try:
                    file_path = self._generate_enumeration_class(enum)
                    generated_files.append(file_path)
                except Exception as e:
                    print(f"Greška pri generisanju enumeracije {enum.name}: {e}")
        
        # Generiši entitete
        if not hasattr(self.model, 'classes') or self.model.classes is None:
            return generated_files
        
        for cls in self.model.classes:
            try:
                file_path = self._generate_entity_class(cls)
                generated_files.append(file_path)
            except Exception as e:
                print(f"Greška pri generisanju klase {cls.name}: {e}")
        
        return generated_files
    
    def _generate_enumeration_class(self, enum: Enumeration) -> str:
        """Generiši Java enumeraciju"""
        enum_values = []
        
        if hasattr(enum, 'literals') and enum.literals:
            for literal in enum.literals:
                enum_values.append(literal.name if hasattr(literal, 'name') else str(literal))
        
        enum_code = f"""package {self.package_name};

/**
 * Enumeracija {enum.name}
 * 
 * Generirano automatski od BESSER B-UML modela
 * 
 * @author Spring Entity Generator
 * @version 1.0
 */
public enum {enum.name} {{
"""
        
        for i, value in enumerate(enum_values):
            enum_code += f"    {value}"
            if i < len(enum_values) - 1:
                enum_code += ",\n"
            else:
                enum_code += ";\n"
        
        enum_code += f"""
    /**
     * Pronađi enumeraciju po imenu
     * 
     * @param value String vrednost
     * @return {enum.name} enumeracija
     */
    public static {enum.name} fromValue(String value) {{
        try {{
            return valueOf(value.toUpperCase());
        }} catch (IllegalArgumentException e) {{
            return null;
        }}
    }}
}}
"""
        
        # Napiši datoteku
        file_path = self.output_path / f"{enum.name}.java"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(enum_code)
        
        return str(file_path)
    
    def _generate_entity_class(self, buml_class: Class) -> str:
        """Generiši jednu Spring Entity klasu"""
        
        # Pripremi podatke za template
        context = {
            'class_name': buml_class.name,
            'package_name': self.package_name,
            'table_name': self._to_snake_case(buml_class.name),
            'parent': self._get_parent_class(buml_class),
            'is_abstract': self._is_abstract_class(buml_class),
            'description': self._get_description(buml_class),
            'imports': self._generate_imports(buml_class),
            'attributes': self._prepare_attributes(buml_class),
            'relations': self._prepare_relations(buml_class),
            'unique_constraints': self._prepare_unique_constraints(buml_class),
            'constructor_params': self._generate_constructor_params(buml_class),
            'constructor_params_list': self._generate_constructor_params_list(buml_class),
            'constructor_assignments': self._generate_constructor_assignments(buml_class),
            'getters_setters': self._prepare_getters_setters(buml_class),
        }
        
        # Učitaj i primeni template
        template = self.jinja_env.get_template('entity_template.j2')
        entity_code = template.render(**context)
        
        # Napiši datoteku
        file_path = self.output_path / f"{buml_class.name}.java"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(entity_code)
        
        return str(file_path)
    
    def _is_abstract_class(self, buml_class: Class) -> bool:
        """Proverite da li je klasa apstraktna"""
        return hasattr(buml_class, 'is_abstract') and buml_class.is_abstract
    
    def _get_parent_class(self, buml_class: Class) -> Optional[str]:
        """Pronađi parent klasu ako postoji generalizacija"""
        if hasattr(buml_class, 'parents') and buml_class.parents:
            parents = buml_class.parents
            if parents:
                parent = list(parents)[0]
                return parent.name
        return None
    
    def _get_description(self, buml_class: Class) -> Optional[str]:
        """Preuzmi opis klase"""
        if hasattr(buml_class, 'metadata') and buml_class.metadata:
            if hasattr(buml_class.metadata, 'description'):
                return buml_class.metadata.description
        return None
    
    def _get_visibility(self, element) -> str:
        """Preuzmi visibility modifier"""
        visibility = "private"  # Default
        
        if hasattr(element, 'visibility'):
            vis = element.visibility
            if vis is None:
                visibility = "public"
            elif isinstance(vis, str):
                vis_lower = vis.lower()
                if 'public' in vis_lower:
                    visibility = "public"
                elif 'protected' in vis_lower:
                    visibility = "protected"
                elif 'private' in vis_lower:
                    visibility = "private"
            else:
                # Ako je VisibilityKind enum
                try:
                    if hasattr(vis, 'name'):
                        vis_name = vis.name.lower()
                        if 'public' in vis_name:
                            visibility = "public"
                        elif 'protected' in vis_name:
                            visibility = "protected"
                        elif 'private' in vis_name:
                            visibility = "private"
                except:
                    pass
        
        return visibility
    
    def _generate_imports(self, buml_class: Class) -> List[str]:
        """Generiši potrebne Java importe"""
        imports = set([
            "jakarta.persistence.Entity",
            "jakarta.persistence.Table",
            "jakarta.persistence.Id",
            "jakarta.persistence.GeneratedValue",
            "jakarta.persistence.GenerationType",
            "jakarta.persistence.Column",
            "jakarta.persistence.OneToOne",
            "jakarta.persistence.OneToMany",
            "jakarta.persistence.ManyToOne",
            "jakarta.persistence.ManyToMany",
            "jakarta.persistence.JoinColumn",
            "jakarta.persistence.JoinTable",
            "jakarta.persistence.FetchType",
            "jakarta.persistence.CascadeType",
            "jakarta.persistence.Enumerated",
            "jakarta.persistence.EnumType",
            "jakarta.persistence.UniqueConstraint",
            "java.time.LocalDate",
            "java.time.LocalDateTime",
            "java.util.HashSet",
            "java.util.Set",
            "java.util.Objects",
        ])
        
        # Dodaj inheritance import ako je potrebna
        if self._is_abstract_class(buml_class):
            imports.add("jakarta.persistence.Inheritance")
            imports.add("jakarta.persistence.InheritanceType")
        
        # Dodaj importe na osnovu atributa
        if buml_class.attributes:
            for attr in buml_class.attributes:
                if self._is_readonly_attribute(attr):
                    imports.add("org.hibernate.annotations.Immutable")
                
                if self._is_enum_attribute(attr):
                    enum_type = self._get_enum_name(attr.type)
                    imports.add(f"{self.package_name}.{enum_type}")
                elif hasattr(attr.type, 'name'):
                    type_name = attr.type.name
                    if 'BigDecimal' in type_name:
                        imports.add("java.math.BigDecimal")
                    if 'UUID' in type_name:
                        imports.add("java.util.UUID")
        
        return sorted(list(imports))
    
    def _is_readonly_attribute(self, attr: Property) -> bool:
        """Proverite da li je atribut readonly"""
        return hasattr(attr, 'is_read_only') and attr.is_read_only
    
    def _is_derived_attribute(self, attr: Property) -> bool:
        """Proverite da li je atribut izvedena vrednost"""
        return hasattr(attr, 'is_derived') and attr.is_derived
    
    def _is_enum_attribute(self, attr: Property) -> bool:
        """Proverite da li je atribut enumeracija"""
        if hasattr(attr, 'type') and attr.type:
            type_name = attr.type.name if hasattr(attr.type, 'name') else str(attr.type)
            return type_name in self.enumerations
        return False
    
    def _get_enum_name(self, attr_type) -> str:
        """Preuzmi naziv enumeracije"""
        if hasattr(attr_type, 'name'):
            return attr_type.name
        return str(attr_type)
    
    def _prepare_attributes(self, buml_class: Class) -> List[Dict]:
        """Pripremi podatke za atribute"""
        attributes = []
        
        if not buml_class.attributes:
            return attributes
        
        for attr in buml_class.attributes:
            if self._is_association_end(attr):
                continue
            
            # Proverite da li je ovo ID polje
            is_id = hasattr(attr, 'is_id') and attr.is_id
            
            # Visibility
            visibility = self._get_visibility(attr)
            
            # Readonly
            is_readonly = self._is_readonly_attribute(attr)
            
            # Derived
            is_derived = self._is_derived_attribute(attr)
            
            # Enumeracija
            is_enum = self._is_enum_attribute(attr)
            
            java_type = self._map_type_to_java(attr.type)
            column_name = self._to_snake_case(attr.name)
            
            # Nullable
            nullable = True
            if hasattr(attr, 'lower') and attr.lower == 1:
                nullable = False
            
            # Length
            length = None
            if java_type == 'String':
                length = 255
            
            # Unique
            unique = False
            if 'email' in attr.name.lower() or 'username' in attr.name.lower():
                unique = True
            
            # Opis
            description = None
            if hasattr(attr, 'metadata') and attr.metadata:
                if hasattr(attr.metadata, 'description'):
                    description = attr.metadata.description
            
            # Default vrednost
            default_value = None
            if hasattr(attr, 'default_value'):
                default_value = attr.default_value
            
            # Updatable/Insertable
            updatable = None
            insertable = None
            
            if is_readonly:
                updatable = False
            
            if is_id or is_derived:
                insertable = False
            
            # Enum vrednosti
            enum_values = None
            if is_enum:
                enum_name = self._get_enum_name(attr.type)
                if enum_name in self.enumerations:
                    enum = self.enumerations[enum_name]
                    if hasattr(enum, 'literals'):
                        enum_values = [lit.name if hasattr(lit, 'name') else str(lit) for lit in enum.literals]
            
            attributes.append({
                'name': attr.name,
                'java_type': java_type,
                'column_name': column_name,
                'visibility': visibility,
                'nullable': nullable,
                'unique': unique,
                'length': length,
                'is_id': is_id,
                'is_enum': is_enum,
                'is_readonly': is_readonly,
                'is_derived': is_derived,
                'description': description,
                'default_value': default_value,
                'updatable': updatable,
                'insertable': insertable,
                'enum_values': ", ".join(enum_values) if enum_values else None
            })
        
        return attributes
    
    def _prepare_relations(self, buml_class: Class) -> List[Dict]:
        """Pripremi podatke za relacije"""
        relations = []
        
        if buml_class.name not in self.associations_by_class:
            return relations
        
        for assoc in self.associations_by_class[buml_class.name]:
            source_end = None
            target_end = None
            
            if hasattr(assoc, 'ends') and assoc.ends:
                for end in assoc.ends:
                    if hasattr(end, 'type') and end.type == buml_class:
                        source_end = end
                    else:
                        target_end = end
            
            if not source_end or not target_end:
                continue
            
            relation_type = self._determine_relation_type(source_end, target_end)
            target_class = target_end.type.name if hasattr(target_end, 'type') else "Unknown"
            field_name = self._to_camel_case_first_lower(target_class)
            plural_name = self._pluralize(field_name)
            plural_name_capitalized = self._capitalize_first(plural_name)
            
            # Visibility
            visibility = self._get_visibility(source_end)
            
            # Navigable
            is_navigable = hasattr(source_end, 'is_navigable') and source_end.is_navigable
            
            # Owning side
            is_owning_side = relation_type in ["ManyToOne", "ManyToMany"]
            
            # Cascade types
            cascade_types = ["PERSIST", "MERGE"]
            if relation_type == "OneToMany":
                cascade_types = ["ALL"]
            
            # Fetch type
            fetch_type = "LAZY"
            
            # Optional
            is_optional = True
            if relation_type in ["ManyToOne"]:
                if hasattr(target_end, 'lower') and target_end.lower == 1:
                    is_optional = False
            
            # Opis
            description = None
            if hasattr(source_end, 'metadata') and source_end.metadata:
                if hasattr(source_end.metadata, 'description'):
                    description = source_end.metadata.description
            
            side_description = "OWNING SIDE" if is_owning_side else "INVERSE SIDE"
            cascade_types_str = ", ".join(cascade_types)
            
            relation_data = {
                'type': relation_type,
                'target_class': target_class,
                'field_name': field_name,
                'plural_name': plural_name,
                'plural_name_capitalized': plural_name_capitalized,
                'join_column_name': self._to_snake_case(field_name) + '_id',
                'mapped_by': self._to_camel_case_first_lower(buml_class.name),
                'source_class': buml_class.name,
                'join_table_name': f"{self._to_snake_case(buml_class.name)}_{self._to_snake_case(target_class)}",
                'source_join_column': f"{self._to_snake_case(buml_class.name)}_id",
                'target_join_column': f"{self._to_snake_case(target_class)}_id",
                'visibility': visibility,
                'is_owning_side': is_owning_side,
                'is_navigable': is_navigable,
                'cascade_types': cascade_types,
                'cascade_types_str': cascade_types_str,
                'fetch_type': fetch_type,
                'is_optional': is_optional,
                'side_description': side_description,
                'description': description
            }
            
            relations.append(relation_data)
        
        return relations
    
    def _prepare_unique_constraints(self, buml_class: Class) -> List[Dict]:
        """Pripremi podatke za unique constraints"""
        constraints = []
        
        if not buml_class.attributes:
            return constraints
        
        unique_attrs = []
        for attr in buml_class.attributes:
            if self._is_association_end(attr):
                continue
            
            if 'email' in attr.name.lower() or 'username' in attr.name.lower():
                unique_attrs.append(attr.name)
        
        if unique_attrs:
            constraint = {
                'name': f"uk_{self._to_snake_case(buml_class.name)}_{'_'.join([self._to_snake_case(a) for a in unique_attrs])}",
                'columns': ', '.join([f'"{self._to_snake_case(a)}"' for a in unique_attrs])
            }
            constraints.append(constraint)
        
        return constraints
    
    def _generate_constructor_params(self, buml_class: Class) -> str:
        """Generiši parametre za konstruktor"""
        all_attrs = self._get_all_attributes(buml_class)
        
        if not all_attrs:
            return ""
        
        params = []
        for attr in all_attrs:
            java_type = self._map_type_to_java(attr.type)
            attr_name = attr.name if hasattr(attr, 'name') else "unknown"
            params.append(f"{java_type} {attr_name}")
        
        return ", ".join(params)
    
    def _generate_constructor_params_list(self, buml_class: Class) -> List[Dict]:
        """Generiši listu parametara sa tipom"""
        all_attrs = self._get_all_attributes(buml_class)
        params = []
        
        for attr in all_attrs:
            java_type = self._map_type_to_java(attr.type)
            attr_name = attr.name if hasattr(attr, 'name') else "unknown"
            params.append({
                'name': attr_name,
                'type': java_type
            })
        
        return params
    
    def _generate_constructor_assignments(self, buml_class: Class) -> List[str]:
        """Generiši dodele vrednosti u konstruktoru"""
        all_attrs = self._get_all_attributes(buml_class)
        assignments = []
        
        for attr in all_attrs:
            attr_name = attr.name if hasattr(attr, 'name') else "unknown"
            assignments.append(f"this.{attr_name} = {attr_name};")
        
        return assignments
    
    def _get_all_attributes(self, buml_class: Class) -> List:
        """Preuzmi sve atribute (i obične i relacijske)"""
        all_attrs = []
        
        if buml_class.attributes:
            for attr in buml_class.attributes:
                if not self._is_association_end(attr):
                    all_attrs.append(attr)
        
        if buml_class.name in self.associations_by_class:
            for assoc in self.associations_by_class[buml_class.name]:
                for end in assoc.ends:
                    if hasattr(end, 'type') and end.type != buml_class:
                        all_attrs.append(end)
                        break
        
        return all_attrs
    
    def _prepare_getters_setters(self, buml_class: Class) -> List[Dict]:
        """Pripremi podatke za getter i setter metode"""
        getters_setters = []
        
        if not buml_class.attributes:
            return getters_setters
        
        for attr in buml_class.attributes:
            if self._is_association_end(attr):
                continue
            
            java_type = self._map_type_to_java(attr.type)
            attr_name = attr.name if hasattr(attr, 'name') else "unknown"
            method_name = self._capitalize_first(attr_name)
            visibility = self._get_visibility(attr)
            
            getters_setters.append({
                'java_type': java_type,
                'attribute_name': attr_name,
                'method_name': method_name,
                'visibility': visibility
            })
        
        return getters_setters
    
    def _is_association_end(self, attr: Property) -> bool:
        """Proverite da li je atribut asocijacijski kraj"""
        if hasattr(attr, 'type') and attr.type:
            type_name = attr.type.name if hasattr(attr.type, 'name') else str(attr.type)
            return type_name[0].isupper() and type_name not in self.JAVA_TYPE_MAPPING
        return False
    
    def _map_type_to_java(self, buml_type) -> str:
        """Mapira B-UML tip na Java tip"""
        if buml_type is None:
            return "Object"
        
        type_name = buml_type.name if hasattr(buml_type, 'name') else str(buml_type)
        
        if type_name in self.enumerations:
            return type_name
        
        return self.JAVA_TYPE_MAPPING.get(type_name, type_name)
    
    def _determine_relation_type(self, source_end, target_end) -> str:
        """Odredi tip relacije na osnovu multipliciteta"""
        source_mult = self._get_multiplicity(source_end)
        target_mult = self._get_multiplicity(target_end)
        
        if target_mult in ["0..1", "1"]:
            if source_mult in ["0..*", "*"]:
                return "ManyToOne"
            return "OneToOne"
        elif target_mult in ["0..*", "*"]:
            if source_mult in ["0..*", "*"]:
                return "ManyToMany"
            return "OneToMany"
        
        return "ManyToOne"
    
    def _get_multiplicity(self, end) -> str:
        """Pronađi multipliciteta asocijacionog kraja"""
        if hasattr(end, 'multiplicity') and end.multiplicity:
            mult = end.multiplicity
            if hasattr(mult, 'lower') and hasattr(mult, 'upper'):
                if mult.upper == -1:
                    return f"{mult.lower}..*"
                return f"{mult.lower}..{mult.upper}"
        return "0..1"
    
    @staticmethod
    def _to_snake_case(name: str) -> str:
        """Konvertuje CamelCase u snake_case"""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    @staticmethod
    def _to_camel_case_first_lower(name: str) -> str:
        """Konvertuje CamelCase u camelCase"""
        if not name:
            return name
        return name[0].lower() + name[1:]
    
    @staticmethod
    def _capitalize_first(name: str) -> str:
        """Velikim baš prvi karakter"""
        if not name:
            return name
        return name[0].upper() + name[1:]
    
    @staticmethod
    def _pluralize(name: str) -> str:
        """Pluralizuje ime"""
        if name.endswith('y'):
            return name[:-1] + 'ies'
        elif name.endswith(('s', 'x', 'z', 'ch', 'sh')):
            return name + 'es'
        else:
            return name + 's'