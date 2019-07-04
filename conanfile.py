#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class OggConan(ConanFile):
    name = "ogg"
    version = "1.3.3"
    description = "The OGG library"
    topics = "conan", "ogg", "codec", "audio", "lossless",
    url = "https://github.com/bincrafters/conan-ogg"
    author = "bincrafters <bincrafters@gmail.com>"
    homepage = "https://github.com/xiph/ogg"
    license = "BSD-2-Clause"
    exports = ["LICENSE.md", "FindOGG.cmake"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    _source_subfolder = "sources"
    settings = "os", "arch", "build_type", "compiler"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {'shared': False, 'fPIC': True}

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        url = "{0}/archive/v{1}.tar.gz".format(self.homepage, self.version)
        tools.get(url, sha256="e90a47bb9f9fd490644f82a097c920738de6bfcbd2179ec354e11a2cd3b49806")
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        cmake = CMake(self)
        if self.settings.os != "Windows":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("FindOGG.cmake")
        self.copy("COPYING", src=self._source_subfolder, dst="licenses", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['ogg']

