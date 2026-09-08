"""
Jednostavna proba Spring Entity Generatora - sa apsolutnom putanjom
"""

from datetime import datetime
import sys
import os
from pathlib import Path

from besser.BUML.metamodel.structural.structural import (
    BinaryAssociation, BooleanType, DateTimeType, DateType, DomainModel, Class, FloatType, Generalization, IntegerType, Method, MethodImplementationType, Multiplicity, Parameter, Property, StringType, TimeDeltaType, TimeType, Type, Association, Enumeration, EnumerationLiteral
)
from besser.generators.spring.spring_entity_generator import SpringEntityGenerator
from besser.generators.spring.spring_backend_generator import SpringBackendGenerator
from besser.utilities.web_modeling_editor.backend.services.converters.buml_to_json.class_diagram_converter import class_buml_to_json

def proba_jednostavna_klasa():
    current_dir = Path(__file__).parent
    output_dir = current_dir / "generated/entity"
    output_dir.mkdir(exist_ok=True)

    role = Enumeration(name="Role", literals={EnumerationLiteral(name="USER"), EnumerationLiteral(name="ADMIN")})
    hand = Enumeration(name="Hand", literals={EnumerationLiteral(name="LEFT"), EnumerationLiteral(name="RIGHT")})

    # address = Class(name="Address")
    # address.add_attribute(Property(name="id", type=IntegerType, is_id=True))
    
    user = Class(name="User")
    user.add_attribute(Property(name="id", type=IntegerType, is_id=True))
    user.add_attribute(Property(name="email", type=StringType, is_optional=True, default_value="mikica"))
    # user.add_attribute(Property(name="firstName", type=StringType, is_optional=True, default_value="John"))
    user.add_attribute(Property(name="age", type=IntegerType, default_value=2))
    user.add_attribute(Property(name="role", type=role, visibility="private", default_value="ADMIN"))
    user.add_attribute(Property(name="birthday", type=DateType, visibility="protected", default_value={
        "year": 2056,
        "month": 10,
        "day": 30,
        "hour": 16,
        "minute": 30,
        "second": 27
    }))
    user.add_attribute(Property(name="birthday2", type=TimeType, visibility="protected"))
    # user.add_attribute(Property(name="hand", type=hand))
    user.add_attribute(Property(name="nicknames", type=FloatType, multiplicity=Multiplicity(0, "*"), default_value="1.2f, 3.2f"))
    # user.add_attribute(Property(name="address", type=address, visibility="protected"))

    thing = Class(name="Thing", is_abstract=True)

    computer = Class(name="Computer")
    computer.add_attribute(Property(name="id", type=IntegerType, is_id=True))
    computer.add_attribute(Property(name="model", type=StringType))

    method1 = Method("destroyComputer", visibility="private", parameters=[
        Parameter("when", DateTimeType),
        Parameter("how", StringType)
    ])
    method2 = Method("makeComputer", visibility="private", parameters=[
        Parameter("when", role)
    ], type=DateTimeType)
    computer.add_method(method1)
    computer.add_method(method2)
    
    gen1 = Generalization(general=thing, specific=computer)
    # a = datetime(2026, 11, 20, 16, 13, 22)
    # a.
    # assoc = BinaryAssociation(name="onetoone", ends={
    #     Property(name="computer", type=computer, multiplicity=Multiplicity(1, 1), is_navigable=True),
    #     Property(name="owner", type=user, multiplicity=Multiplicity(1, 1), is_navigable=False)
    # })

    assoc = BinaryAssociation(name="onetomany", ends={
        Property(name="ownerr", type=user, multiplicity=Multiplicity(1, 1), is_navigable=True),
        Property(name="computers", type=computer, multiplicity=Multiplicity(0, "*"), is_navigable=True)
    })

    # assoc2 = BinaryAssociation(name="manytoone", ends={
    #     Property(name="computerss", type=computer, multiplicity=Multiplicity(0, "*"), is_navigable=True),
    #     Property(name="ownerr", type=user, multiplicity=Multiplicity(1, 1), is_navigable=True)
    # })

    # assoc = BinaryAssociation(name="ManyToMany", ends={
    #     Property(name="computers", type=computer, multiplicity=Multiplicity(0, "*"), is_navigable=True),
    #     Property(name="owners", type=user, multiplicity=Multiplicity(0, "*"), is_navigable=True)
    # })

    model = DomainModel(name="proba", types={user, thing, computer, role, hand}, generalizations={gen1}, associations={assoc})

    # generator = SpringEntityGenerator(
    #     model,
    #     output_dir=output_dir,
    #     package_name="spring.entities"
    # )

    generator = SpringBackendGenerator(
        model, "3.5.11", java_version="17", app_name="Example", output_dir=current_dir / "backend2", package_name="com.example.faculty"
    )
    
    files = generator.generate()

    # json_model = class_buml_to_json(model)

    # import requests

    # res = requests.post("http://localhost:9000/besser_api/generate-output", json={
    #     "title": "spring backendaa",
    #     "config": {
    #         "spring_boot_version": "3.5.11",
    #         "java_version": "17",
    #         "app_name": "Transformers",
    #         "package_name": "com.transformers",
    #         "project_name": "trans"
    #     },
    #     "model": {
    #         "elements": json_model["elements"],
    #         "relationships": json_model["relationships"]
    #     },
    #     "generator": "spring"
    # })
    
    # if res.status_code == 200:
    #     with open("project.zip", "wb") as f:
    #         f.write(res.content)

    #     print("ZIP sacuvan kao project.zip")
    # else:
    #     print(res.status_code, res.text)

def proba():
    # Classes
    Patient = Class(name="Patient")
    Medicine = Class(name="Medicine")
    PatientFile = Class(name="PatientFile")
    Person = Class(name="Person", is_abstract=True)
    Doctor = Class(name="Doctor")

    # Patient class attributes and methods
    Patient_patientId: Property = Property(name="patientId", type=StringType)
    Patient.attributes={Patient_patientId}

    # Medicine class attributes and methods
    Medicine_id: Property = Property(name="id", type=IntegerType, is_id=True)
    Medicine_name: Property = Property(name="name", type=StringType)
    Medicine_m_heal: Method = Method(name="heal", parameters={}, implementation_type=MethodImplementationType.NONE)
    Medicine.attributes={Medicine_id, Medicine_name}
    Medicine.methods={Medicine_m_heal}

    # PatientFile class attributes and methods
    PatientFile_text: Property = Property(name="text", type=StringType, default_value="This is patient file template text.")
    PatientFile_id: Property = Property(name="id", type=IntegerType, is_id=True)
    PatientFile.attributes={PatientFile_id, PatientFile_text}

    # Person class attributes and methods
    Person_id: Property = Property(name="id", type=IntegerType, is_id=True)
    Person_name: Property = Property(name="name", type=StringType)
    Person_birthday: Property = Property(name="birthday", type=DateType, is_optional=True)
    Person.attributes={Person_birthday, Person_id, Person_name}

    # Doctor class attributes and methods
    Doctor_isDirector: Property = Property(name="isDirector", type=BooleanType)
    Doctor_calling: Property = Property(name="calling", type=StringType)
    Doctor.attributes={Doctor_calling, Doctor_isDirector}

    # Relationships
    person_medicine: BinaryAssociation = BinaryAssociation(
        name="person_medicine",
        ends={
            Property(name="patient", type=Patient, multiplicity=Multiplicity(0, 9999), is_navigable=False),
            Property(name="consumes", type=Medicine, multiplicity=Multiplicity(0, 9999))
        }
    )
    person_person_file: BinaryAssociation = BinaryAssociation(
        name="person_person_file",
        ends={
            Property(name="patientfile", type=PatientFile, multiplicity=Multiplicity(1, 1), is_navigable=False),
            Property(name="owner", type=Patient, multiplicity=Multiplicity(1, 1))
        }
    )
    Doctor_Patient: BinaryAssociation = BinaryAssociation(
        name="Doctor_Patient",
        ends={
            Property(name="doctors", type=Doctor, multiplicity=Multiplicity(1, 9999)),
            Property(name="patients", type=Patient, multiplicity=Multiplicity(1, 9999))
        }
    )

    # Generalizations
    gen_Patient_Person = Generalization(general=Person, specific=Patient)
    gen_Doctor_Person = Generalization(general=Person, specific=Doctor)

    # Domain Model
    domain_model = DomainModel(
        name="Class_Diagram",
        types={Patient, Medicine, PatientFile, Person, Doctor},
        associations={person_medicine, person_person_file, Doctor_Patient},
        generalizations={gen_Patient_Person, gen_Doctor_Person},
        metadata=None
    )

    current_dir = Path(__file__).parent
    generator = SpringBackendGenerator(
        domain_model, "3.5.11", java_version="17", app_name="Hospital", output_dir=current_dir / "hospital", group_id="com.hospital", package_name="com.hospital"
    )
    
    files = generator.generate()

if __name__ == "__main__":
    proba()