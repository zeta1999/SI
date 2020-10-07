from conans import ConanFile, CMake, tools
from conans.tools import load
from conans.errors import ConanInvalidConfiguration
import re, os


class SiConan(ConanFile):
    name = "SI"
    license = "MIT"
    url = "https://bintray.com/beta/#/bernedom/conan/SI:SI"
    homepage = "https://github.com/bernedom/SI"
    description = "A header only c++ library that provides type safety and user defined literals \
         for handling pyhsical values defined in the International System of Units."
    topics = ("physical units", "SI-unit-conversion",
              "cplusplus-library", "cplusplus-17")
    exports_sources = "include/*", "CMakeLists.txt", "test/*", "doc/CMakeLists.txt", "doc/*.md", "cmake/SIConfig.cmake.in", "LICENSE"
    no_copy_source = True
    generators = "cmake", "txt", "cmake_find_package"
    settings = "os", "arch", "compiler", "build_type"
    build_requires = "Catch2/2.11.1@catchorg/stable"
    _cmake = None

    def _configure_cmake(self):
        if self._cmake is None:
            self._cmake = CMake(self)
            # Add additional settings with cmake.definitions["SOME_DEFINITION"] = True
            self._cmake.configure()
        return self._cmake

    @property
    def _compilers_minimum_version(self):
        return {
            "gcc": "7",
            "Visual Studio": "15",
            "clang": "5",
            "apple-clang": "10",
        }

    def configure(self):
        if self.settings.compiler.get_safe("cppstd"):
            tools.check_min_cppstd(self, "17")
        minimum_version = self._compilers_minimum_version.get(
            str(self.settings.compiler), False)
        if minimum_version:
            if tools.Version(self.settings.compiler.version) < minimum_version:
                raise ConanInvalidConfiguration("bertrand requires C++17, which your compiler ({} {}) does not support.".format(
                    self.settings.compiler, self.settings.compiler.version))
        else:
            self.output.warn(
                "SI requires C++17. Your compiler is unknown. Assuming it supports C++17.")        

    def set_version(self):
        cmake = load(os.path.join(self.recipe_folder, "CMakeLists.txt"))
        
        version = re.search(r"(?:[ \t]*)(?:VERSION\s+?)(\d+\.\d+\.\d+)", cmake).group(1)
        self.version = version


    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def test(self):
        cmake = self._configure_cmake()
        cmake.test()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_id(self):
        self.info.header_only()
