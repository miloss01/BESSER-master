import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from besser.BUML.metamodel.structural.structural import DomainModel
from besser.generators.generator_interface import GeneratorInterface
from besser.generators.spring.spring_controller_generator import SpringControllerGenerator
from besser.generators.spring.spring_entity_generator import SpringEntityGenerator
from besser.generators.spring.spring_http_generator import SpringHttpGenerator
from besser.generators.spring.spring_repository_generator import SpringRepositoryGenerator
from besser.generators.spring.spring_service_generator import SpringServiceGenerator

class SpringBackendGenerator(GeneratorInterface):
    
    def __init__(self, 
                 model: DomainModel, 
                 spring_boot_version: str,
                 java_version: str,
                 app_name: str,
                 output_dir: str,
                 package_name: str = "com.example",
                 group_id: str = "com.example",
                 description: str = ""
                ):
        super().__init__(model, output_dir)

        self.package_name = package_name
        self.spring_boot_version = spring_boot_version
        self.java_version = java_version
        self.app_name = app_name
        self.group_id = group_id
        self.description = description

    def generate(self):
        self._generate_pom_file()
        self._generate_mvn_files()
        self._generate_main_and_test_files()
        self._generate_properties_file()
        self._generate_entities()
        self._generate_repositories()
        self._generate_services()
        self._generate_controllers()
        self._generate_http()

    def _generate_pom_file(self):
        file_path = self.build_generation_path(file_name="pom.xml")
        templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        env = Environment(loader=FileSystemLoader(templates_path))
        pom_template = env.get_template("pom.xml.j2")

        context = {
            "name": self.app_name,
            "spring_boot_version": self.spring_boot_version,
            "group_id": self.group_id,
            "description": self.description,
            "java_version": self.java_version
        }

        with open(file_path, mode="w", encoding="utf-8") as f:
            generated_code = pom_template.render(**context)
            f.write(generated_code)

    def _generate_mvn_files(self):
        templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        env = Environment(loader=FileSystemLoader(templates_path))

        file_path = self.build_generation_path(file_name=Path(self.output_dir, ".mvn", "wrapper", "maven-wrapper.properties"))
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        maven_wrapper_template = env.get_template("maven-wrapper.properties.j2")

        with open(file_path, mode="w", encoding="utf-8") as f:
            generated_code = maven_wrapper_template.render()
            f.write(generated_code)

        file_path = self.build_generation_path(file_name=Path(self.output_dir, ".mvn", "mvnw"))
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        mvnw_template = env.get_template("mvnw.j2")

        with open(file_path, mode="w", encoding="utf-8") as f:
            generated_code = mvnw_template.render()
            f.write(generated_code)

        file_path = self.build_generation_path(file_name=Path(self.output_dir, ".mvn", "mvnw.cmd"))
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        mvnw_cmd_template = env.get_template("mvnw.cmd.j2")

        with open(file_path, mode="w", encoding="utf-8") as f:
            generated_code = mvnw_cmd_template.render()
            f.write(generated_code)

    def _generate_main_and_test_files(self):
        templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        env = Environment(loader=FileSystemLoader(templates_path))

        file_path = self.build_generation_path(file_name=Path("src", "main", "java") / Path().joinpath(*self.package_name.split(".")) / f"{self.app_name[0].upper() + self.app_name[1:]}.java")
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        main_template = env.get_template("main.java.j2")

        context = {
            "name": self.app_name,
            "package": self.package_name
        }

        with open(file_path, mode="w", encoding="utf-8") as f:
            generated_code = main_template.render(**context)
            f.write(generated_code)

        file_path = self.build_generation_path(file_name=Path("src", "test", "java") / Path().joinpath(*self.package_name.split(".")) / f"{self.app_name[0].upper() + self.app_name[1:]}Tests.java")
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        test_template = env.get_template("test.java.j2")

        context = {
            "name": self.app_name,
            "package": self.package_name
        }

        with open(file_path, mode="w", encoding="utf-8") as f:
            generated_code = test_template.render(**context)
            f.write(generated_code)

    def _generate_properties_file(self):
        file_path = self.build_generation_path(file_name=Path("src", "main", "resources", "application.properties"))
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        env = Environment(loader=FileSystemLoader(templates_path))
        app_properties_template = env.get_template("application.properties.j2")

        context = {
            "name": self.app_name,
        }

        with open(file_path, mode="w", encoding="utf-8") as f:
            generated_code = app_properties_template.render(**context)
            f.write(generated_code)

    def _generate_entities(self):
        generator = SpringEntityGenerator(
            self.model,
            output_dir=self.output_dir / Path("src", "main", "java") / Path().joinpath(*self.package_name.split(".")) / "entity",
            package_name=f"{self.package_name}.entity"
        )

        generator.generate()

    def _generate_repositories(self):
        generator = SpringRepositoryGenerator(
            self.model,
            f"{self.package_name}.entity",
            output_dir=self.output_dir / Path("src", "main", "java") / Path().joinpath(*self.package_name.split(".")) / "repository",
            package_name=f"{self.package_name}.repository"
        )

        generator.generate()

    def _generate_services(self):
        generator = SpringServiceGenerator(
            self.model,
            f"{self.package_name}.entity",
            f"{self.package_name}.repository",
            output_dir=self.output_dir / Path("src", "main", "java") / Path().joinpath(*self.package_name.split(".")) / "service",
            package_name=f"{self.package_name}.service"
        )

        generator.generate()

    def _generate_controllers(self):
        generator = SpringControllerGenerator(
            self.model,
            f"{self.package_name}.entity",
            f"{self.package_name}.service",
            output_dir=self.output_dir / Path("src", "main", "java") / Path().joinpath(*self.package_name.split(".")) / "controller",
            package_name=f"{self.package_name}.controller"
        )

        generator.generate()

    def _generate_http(self):
        generator = SpringHttpGenerator(
            self.model,
            output_dir=self.output_dir / Path("src", "main", "java") / Path().joinpath(*self.package_name.split(".")) / "http_test"
        )

        generator.generate()