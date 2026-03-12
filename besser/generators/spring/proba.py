"""
Jednostavna proba Spring Entity Generatora - sa apsolutnom putanjom
"""

import sys
import os
from pathlib import Path

from besser.BUML.metamodel.structural.structural import (
    BinaryAssociation, DateTimeType, DateType, DomainModel, Class, FloatType, Generalization, IntegerType, Multiplicity, Property, StringType, TimeDeltaType, Type, Association, Enumeration, EnumerationLiteral
)
from besser.generators.spring.spring_entity_generator import SpringEntityGenerator
from besser.generators.spring.spring_backend_generator import SpringBackendGenerator

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
    user.add_attribute(Property(name="email", type=StringType, is_optional=True))
    # user.add_attribute(Property(name="firstName", type=StringType, is_optional=True, default_value="John"))
    user.add_attribute(Property(name="age", type=IntegerType, default_value=2))
    user.add_attribute(Property(name="role", type=role, visibility="private"))
    user.add_attribute(Property(name="birthday", type=TimeDeltaType, visibility="protected"))
    user.add_attribute(Property(name="birthday2", type=DateTimeType, visibility="protected"))
    # user.add_attribute(Property(name="hand", type=hand))
    # user.add_attribute(Property(name="nicknames", type=DateTimeType, multiplicity=Multiplicity(0, "*"), default_value="1.2f, 3.2f"))
    # user.add_attribute(Property(name="address", type=address, visibility="protected"))

    thing = Class(name="Thing", is_abstract=True)

    computer = Class(name="Computer")
    computer.add_attribute(Property(name="id", type=IntegerType, is_id=True))
    computer.add_attribute(Property(name="model", type=StringType))
    
    gen1 = Generalization(general=thing, specific=computer)

    # assoc = BinaryAssociation(name="onetoone", ends={
    #     Property(name="computer", type=computer, multiplicity=Multiplicity(1, 1), is_navigable=True),
    #     Property(name="owner", type=user, multiplicity=Multiplicity(1, 1), is_navigable=False)
    # })

    # assoc = BinaryAssociation(name="onetomany", ends={
    #     Property(name="ownerr", type=user, multiplicity=Multiplicity(1, 1), is_navigable=True),
    #     Property(name="computers", type=computer, multiplicity=Multiplicity(0, "*"), is_navigable=False)
    # })

    # assoc2 = BinaryAssociation(name="manytoone", ends={
    #     Property(name="computerss", type=computer, multiplicity=Multiplicity(0, "*"), is_navigable=True),
    #     Property(name="ownerr", type=user, multiplicity=Multiplicity(1, 1), is_navigable=True)
    # })

    assoc = BinaryAssociation(name="ManyToMany", ends={
        Property(name="computers", type=computer, multiplicity=Multiplicity(0, "*"), is_navigable=True),
        Property(name="owners", type=user, multiplicity=Multiplicity(0, "*"), is_navigable=True)
    })

    model = DomainModel(name="proba", types={user, thing, computer, role, hand}, generalizations={gen1}, associations={assoc})

    # generator = SpringEntityGenerator(
    #     model,
    #     output_dir=output_dir,
    #     package_name="spring.entities"
    # )

    generator = SpringBackendGenerator(
        model, "3.5.11", java_version="17", app_name="Transformers", output_dir=current_dir / "backend", package_name="com.transformers"
    )
    
    files = generator.generate()

if __name__ == "__main__":
    proba_jednostavna_klasa()