"""
Jednostavna proba Spring Entity Generatora - sa apsolutnom putanjom
"""

import sys
import os
from pathlib import Path

from besser.BUML.metamodel.structural.structural import (
    DateTimeType, DomainModel, Class, FloatType, Generalization, IntegerType, Multiplicity, Property, StringType, TimeDeltaType, Type, Association, Enumeration, EnumerationLiteral
)
from besser.generators.spring.generator import SpringEntityGenerator


def proba_jednostavna_klasa():
    current_dir = Path(__file__).parent
    output_dir = current_dir / "generated"
    output_dir.mkdir(exist_ok=True)

    role = Enumeration(name="Role", literals={EnumerationLiteral(name="USER"), EnumerationLiteral(name="ADMIN")})
    hand = Enumeration(name="Hand", literals={EnumerationLiteral(name="LEFT"), EnumerationLiteral(name="RIGHT")})
    
    user = Class(name="User")
    user.add_attribute(Property(name="email", type=StringType, is_id=True, is_optional=True))
    user.add_attribute(Property(name="firstName", type=StringType, is_optional=True, default_value="John"))
    user.add_attribute(Property(name="age", type=IntegerType, default_value=2))
    # user.add_attribute(Property(name="role", type=role, visibility="private"))
    user.add_attribute(Property(name="birthday", type=TimeDeltaType, visibility="protected"))
    # user.add_attribute(Property(name="hand", type=hand))
    user.add_attribute(Property(name="nicknames", type=FloatType, multiplicity=Multiplicity(0, "*"), default_value="1.2f, 3.2f"))

    thing = Class(name="Thing", is_abstract=True)

    computer = Class(name="Computer")
    computer.add_attribute(Property(name="name", type=StringType))
    
    gen1 = Generalization(general=thing, specific=computer)

    model = DomainModel(name="proba", types={user, thing, computer, role, hand}, generalizations={gen1})

    generator = SpringEntityGenerator(
        model,
        output_dir=output_dir,
        package_name="spring.entities"
    )
    
    files = generator.generate()

if __name__ == "__main__":
    proba_jednostavna_klasa()