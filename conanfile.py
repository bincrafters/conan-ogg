from conans import ConanFile, CMake, tools
import os


class OggConan(ConanFile):
    name = "ogg"
    version = "1.3.3"
    description = "The OGG library"
    topics = ("conan", "ogg", "codec", "audio", "lossless")
    url = "https://github.com/bincrafters/conan-ogg"
    homepage = "https://github.com/xiph/ogg"
    license = "BSD-2-Clause"
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "build_type", "compiler"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {'shared': False, 'fPIC': True}

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        url = "{0}/archive/v{1}.tar.gz".format(self.homepage, self.version)
        tools.get(url, sha256="e90a47bb9f9fd490644f82a097c920738de6bfcbd2179ec354e11a2cd3b49806")
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy("COPYING", src=self._source_subfolder, dst="licenses", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['ogg']
