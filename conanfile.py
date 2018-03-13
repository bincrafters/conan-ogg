#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class OggConan(ConanFile):
    name = "ogg"
    version = "1.3.3"
    description="The OGG library"
    url="https://github.com/bincrafters/conan-ogg"
    homepage = "https://github.com/xiph/ogg"
    license = "BSD"
    exports = ["LICENSE.md", "FindOGG.cmake"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    source_subfolder = "sources"
    settings = "os", "arch", "build_type", "compiler"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        cmake = CMake(self)
        if self.settings.os != "Windows":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("FindOGG.cmake")
        self.copy("COPYING", src=self.source_subfolder, dst="licenses", keep_path=False)
        self.copy("LICENSE.md", dst="licenses", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['ogg']

