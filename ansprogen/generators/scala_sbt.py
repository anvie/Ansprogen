'''
Copyright (c) 2011 Ansvia. http://www.ansvia.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import os
import re
from string import Template

from IGenerator import IGenerator, GeneratorException


class ScalaGenerator(IGenerator):	
	
	name = "Scala:sbt"
	source_ext = ".scala"
	parameters = [
		{
			'name': 'name',
			'desc': 'Project name.',
			'data_type': 'string',
			'default': 'Hello'
		},
		{
			'name': 'version',
			'desc': 'Project version.',
			'data_type': 'string',
			'default': '0.0.1'
		},
		{
			'name': 'package',
			'desc': 'Package name, ex: com.mycom.myapp',
			'data_type': 'string',
			'default': None
		},
		{
			'name': 'plugins',
			'desc': 'Plugins index list separated by whitespace. ex: 1 2',
			'data_type': 'list',
			'default': [],
			'accept': ['sbt-assembly', 'xsbt-proguard-plugin', 'sbteclipse']
		}
	]

	
	def __init__(self, out_dir, name="Hello", version="0.0.1", main_class=None, package=None, plugins=[]):
		super(ScalaGenerator, self).__init__(out_dir)
		
		self._build_file = "build.sbt"
		
		if not self._build_file:
			raise GeneratorException, "Unsupported kind `%s`" % kind
		
		self.target_name = name
		
		if main_class:
			self.main_class = main_class.title()
		elif name:
			self.main_class = name
		else:
			self.main_class = "Hello"
		
		self.package = package
		self.version = version
		
		_template_build = [
			'name := "$name"',
			'version := "$version"',
			'scalaVersion := "$scala_version"'
		]
		
		if ' ' in plugins:
			plugins = map(lambda x:_get_sbt_plugin(int(x)), plugins.split(' '))
			
			for PClass in plugins:
				p = PClass(self)
				_template_build += p.sbt_build_stuff
		
		self.plugins = plugins
		
		## shorting, all import* place on top
		def _cmp(a, b):
			if a.startswith("import"):
				return -1
			return 1
		
		_template_build = sorted(_template_build, _cmp)
		self._template_build = Template('\n\n'.join(_template_build))
		
		package = ""
		if self.package:
			package = "package " + self.package
		
		self._template_main = Template('''
%(package)s

object $main_class {

	def main(args: Array[String]): Unit = {

		println("Yo World!")
	
	}

}
''' % dict(package = package))

	
	def generate(self):
		build_file = super(ScalaGenerator, self).generate()
		
		if not build_file:
			print "Aborted."
			return False
		
		self.scala_home = os.environ.get('SCALA_HOME')
		if self.scala_home:
			if os.path.exists(self.scala_home) == False:
				raise GeneratorException, "Scala home not exists `%s`" % self.scala_home
			
			if os.path.isdir(self.scala_home) == False:
				raise GeneratorException, "Scala home is not dir `%s`" % self.scala_home
		
		if not self.scala_home:
			## get scala_home
			dirs = [
				'/opt/local/share/scala-2.9',
				'/usr/local/share/scala',
				'/usr/lib/scala',
				'/usr/local/lib/scala',
				'/opt/lib/scala',
				'/usr/share/lib'
			]
			
			for dir in dirs:
				if os.path.exists(dir + "/lib/scala-library.jar"):
					self.scala_home = dir
					break
		
		## Get scala version
		p = os.popen("scala -version")
		rv = p.readline()
		#from dbgp.client import brk; brk()
		version = re.findall(r'version (\d*?\.\d*?\.\d*?)\.', rv)
		if version and len(version) > 0:
			version = version[0]
		p.close()
		
		self.scala_version = version
		
		self.test()

		#main_class_with_package = self.main_class
		
		if self.package:
			main_class_with_package = self.package + "." + self.main_class

		f = open(build_file, "w")
		data = {
			'name': self.target_name,
			#'package': self.package and self.package or '',
			#'main_class': self.main_class,
			'version': self.version,
			'scala_version': self.scala_version,
			#'main_class_with_package': main_class_with_package
		}
		f.write(self._template_build.substitute(**data))
		f.close()
		
		self.build_main_file()
		
		## Process plugins
		for PClass in self.plugins:
			p = PClass(self)
			p.generate()
			p.close()
		
		return True
	
	def build_main_file(self):
		paths = [self._normalize_path(self.out_dir), "src", "main", "scala"]
		
		if self.package:
			paths += self.package.split(".")
		
		out_dir_ = os.path.join(*paths)
		
		if not os.path.exists(out_dir_):
			os.makedirs(out_dir_)
		
		paths.append(self._normalize_source_name(self.main_class))
		
		main_file = os.path.join(*paths)
		
		f = open(main_file, "w")
		f.write(self._template_main.substitute(
			main_class = self.main_class
		))
		f.close()
		
	@staticmethod
	def usage():
		
		parameters = IGenerator.get_help_parameters(ScalaGenerator)
		
		usage_text = '''
Generate Scala project (sbt)

Parameters:

	%(parameters)s

Examples:

	$ progen -p Scala:sbt -o ./hello name=Hello version=0.0.1 main_class="Hello"
''' % dict(parameters=parameters)
		return usage_text
	


	def rollback(self):
		build_file = os.path.join(self._normalize_path(self.out_dir), self._build_file)
		
		if os.path.exists(build_file):
			os.unlink(build_file)
		
		
	def test(self):
		
		if not self.scala_home:
			raise GeneratorException, "Cannot get scala_home, please set it manually by exporting to SCALA_HOME environment"
		
		if os.path.exists(self.scala_home) == False:
			raise GeneratorException, "Scala home not exists `%s`" % self.scala_home
		
		#if self.kind == "exe" and not self.main_class:
		#	raise GeneratorException, "Scala kind `exe` should have main_class, please set it with main_class parameter."

		if not self.scala_version:
			raise GeneratorException, "Cannot find installed scala"

		return True
		
	
class SbtPlugin(object):
	def __init__(self, generator):
		if not isinstance(generator, IGenerator):
			raise GeneratorException, "Invalid ganerator type passed to SbtPlugin __init__"
		self.gen = generator
		self.sbt_file = None
		
	def close(self):
		if self.sbt_file:
			self.sbt_file.close()
			self.sbt_file = None
	
	def generate(self):
		raise GeneratorException, "Plugin.generate not implemented"
	
	def ensure_plugins_sbt(self):
		p = self.gen._normalize_path(self.gen.out_dir) + "/project"
		
		if not os.path.exists(p):
			os.makedirs(p)
		
		p = p + "/plugins.sbt"
		
		self.sbt_file = None
		if not os.path.exists(p):
			self.sbt_file = open(p, "w")
		else:
			self.sbt_file = open(p, "a")
		
		if not self.sbt_file:
			raise GeneratorException, "Cannot create plugins.sbt file"
			
			

class Assembly(SbtPlugin):
	
	name = "sbt-assembly"
	sbt_build_stuff = [
		'import AssemblyKeys._',
		'seq(assemblySettings: _*)'
	]	
	
	def generate(self):
		self.ensure_plugins_sbt()
		self.sbt_file.write('''addSbtPlugin("com.eed3si9n" % "sbt-assembly" % "0.7.2")\n''')
		self.close()


class Proguard(SbtPlugin):
	
	name = "xsbt-proguard-plugin"

	@property
	def sbt_build_stuff(self):
		rv = [
			'seq(ProguardPlugin.proguardSettings :_*)',
			Template('proguardOptions += keepMain("$package.$main_class")').substitute(package = self.gen.package, main_class=self.gen.main_class)
		]
		return rv
	
	def generate(self):
		self.ensure_plugins_sbt()
		
		p = self.gen._normalize_path(self.gen.out_dir) + "/project/project"
		
		if not os.path.exists(p):
			os.makedirs(p)
		
		p = p + "/Build.scala"
		
		f = None
		
		if os.path.exists(p):
			f = open(p, "a")
		else:
			f = open(p, "w")
		
		f.write('''import sbt._
object PluginDef extends Build {
  override def projects = Seq(root)
  lazy val root = Project("plugins", file(".")) dependsOn(proguard)
  lazy val proguard = uri("git://github.com/siasia/xsbt-proguard-plugin.git")
}
''')
		f.close()
		
		self.close()
		

class Sbtclipse(SbtPlugin):
	
	name = "sbteclipse"
	sbt_build_stuff = []
	
	def generate(self):
		self.ensure_plugins_sbt()
		self.sbt_file.write('''
resolvers += Classpaths.typesafeResolver

addSbtPlugin("com.typesafe.sbteclipse" % "sbteclipse" % "1.5.0")\n''')
		self.close()
	


## Register plugins

_sbt_plugins = [
	Assembly,
	Proguard,
	Sbtclipse
]

def _get_sbt_plugin(i):
	index = i - 1
	if index > len(_sbt_plugins):
		raise GeneratorException, "Unknown SbtPlugin index `%d`" % index
	return _sbt_plugins[index]

	
