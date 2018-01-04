#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os, re


class OggConan(ConanFile):
    name = "ogg"
    version = "1.3.3"
    description="The OGG library"
    url="https://github.com/bincrafters/conan-ogg"
    license="BSD"
    exports = ["LICENSE.md", "FindOGG.cmake"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    source_subfolder = "sources"
    settings = "os", "arch", "build_type", "compiler"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"

    def configure(self):
        del self.settings.compiler.libcxx

        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def source(self):
        source_url = "https://github.com/xiph/ogg"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
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
        self.copy("COPYING", keep_path=False)
        self.copy(pattern="*.h", dst="include/ogg", keep_path=False)
        self.copy(pattern="*.pc", dst=os.path.join('lib', 'pkgconfig'), keep_path=False)

        if self.settings.compiler == "Visual Studio":
            if self.options.shared:
                self.copy(pattern="*.dll", dst="bin", keep_path=False)
            self.copy(pattern="*.pdb", dst="bin", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", keep_path=False)
        else:
            if self.options.shared:
                if self.settings.os == "Macos":
                    self.copy(pattern="*.dylib", dst="lib", keep_path=False)
                elif self.settings.os == "Windows":
                    self.copy(pattern="*.dll", dst="bin", keep_path=False)
                    self.copy(pattern="*.dll.a", dst="lib", keep_path=False)
                else:
                    self.copy(pattern="*.so*", dst="lib", keep_path=False)
            else:
                self.copy(pattern="*g.a", dst="lib", keep_path=False)
     
    def package_info(self):
        self.cpp_info.libs = ['ogg']

    def replace_in_file_regex(file_path, search, replace):
        content = tools.load(file_path)
        content = re.sub(search, replace, content)
        content = content.encode("utf-8")
        tools.save(file_path, content)

