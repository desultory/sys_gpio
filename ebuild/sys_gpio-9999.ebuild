# Copyright 2023-2024 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI=8

DISTUTILS_USE_PEP517=setuptools
PYTHON_COMPAT=( python3_{11..13} )

inherit distutils-r1 git-r3

DESCRIPTION="Simple GPIO library using sysfs"
HOMEPAGE="https://github.com/desultory/sys_gpio"
EGIT_REPO_URI="https://github.com/desultory/${PN}"

LICENSE="GPL-2"
SLOT="0"

RDEPEND="
	>=dev-python/zenlib-9999[${PYTHON_USEDEP}]
"
