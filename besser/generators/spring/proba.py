"""
Jednostavna proba Spring Entity Generatora - sa apsolutnom putanjom
"""

import sys
import os
from pathlib import Path
import tempfile
import shutil

# Dodaj root direktorijum BESSER-a
# root_dir = Path(__file__).parent
# sys.path.insert(0, str(root_dir))

# Uvezi sa eksplicitnom putanjom
from besser.BUML.metamodel.structural.structural import (
    DomainModel, Class, Generalization, Property, Type, Association, Enumeration, EnumerationLiteral
)
from besser.generators.spring.generator import SpringEntityGenerator


def proba_jednostavna_klasa():
    current_dir = Path(__file__).parent
    output_dir = current_dir / "generated"
    output_dir.mkdir(exist_ok=True)
    
    user = Class(name="User")
    user.add_attribute(Property(name="email", type=Type("String")))
    user.add_attribute(Property(name="firstName", type=Type("String")))

    thing = Class(name="Thing", is_abstract=True)

    computer = Class(name="Computer")
    computer.add_attribute(Property(name="name", type=Type("String")))
    
    gen1 = Generalization(general=thing, specific=computer)

    model = DomainModel(name="proba", types={user, thing, computer}, generalizations={gen1})

    generator = SpringEntityGenerator(
        model,
        output_dir=output_dir,
        package_name="spring.entities"
    )
    
    files = generator.generate()

if __name__ == "__main__":
    proba_jednostavna_klasa()