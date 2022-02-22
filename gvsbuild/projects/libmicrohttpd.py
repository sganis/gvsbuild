#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>.

import os

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Libmicrohttpd(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "libmicrohttpd",
            archive_url="http://ftp.gnu.org/gnu/libmicrohttpd/libmicrohttpd-0.9.54.tar.gz",
            hash="bcc721895d4a114b0548a39d2241c35caacb9e2e072d40e11b55c60e3d5ddcbe",
            patches=["001-remove-postsample.patch"],
        )

    def build(self):
        configuration = "release-dll"
        if self.builder.opts.configuration == "debug":
            configuration = "debug-dll"

        td = self.exec_msbuild_gen(
            r"w32", "libmicrohttpd.sln", configuration=configuration
        )
        base_dir = os.path.join("w32", td)

        debug_option = ""
        if self.builder.opts.configuration == "debug":
            debug_option = r"_d"

        rel_dir = ".\\" + base_dir + r"\Output"
        if not self.builder.x86:
            rel_dir += r"\x64"

        self.push_location(rel_dir)
        self.install(r"microhttpd.h include")
        self.install(r"libmicrohttpd-dll" + debug_option + ".lib" + " lib")
        self.install(r"libmicrohttpd-dll" + debug_option + ".dll" + " bin")
        self.install(r"libmicrohttpd-dll" + debug_option + ".pdb" + " bin")
        self.install(r"hellobrowser-dll" + debug_option + ".exe" + " bin")
        self.pop_location()

        self.install(r".\COPYING share\doc\libmicrohttpd")