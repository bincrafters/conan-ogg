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

    def package(self):
        self.copy("FindOGG.cmake")
        self.copy("COPYING", src=self.source_subfolder, keep_path=False)
        self.copy("*.h", dst=os.path.join("include", "ogg"), keep_path=False)
        self.copy("*.pc", dst=os.path.join('lib', 'pkgconfig'), keep_path=False)

        if self.settings.compiler == "Visual Studio":
            if self.options.shared:
                self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.pdb", dst="bin", keep_path=False)
            self.copy("*.lib", dst="lib", keep_path=False)
        else:
            if self.options.shared:
                if self.settings.os == "Macos":
                    self.copy("*.dylib", dst="lib", keep_path=False)
                elif self.settings.os == "Windows":
                    self.copy("*.dll", dst="bin", keep_path=False)
                    self.copy("*.dll.a", dst="lib", keep_path=False)
                else:
                    self.copy("*.so*", dst="lib", keep_path=False)
            else:
                self.copy("*g.a", dst="lib", keep_path=False)
     
    def package_info(self):
        self.cpp_info.libs = ['ogg']

