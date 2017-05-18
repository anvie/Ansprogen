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
from string import Template

from IGenerator import IGenerator, GeneratorException


class ScalaGenerator(IGenerator):	
	
	name = "Scala"
	source_ext = ".scala"
	parameters = [
		{
			'name': 'kind',
			'data_type': 'string',
			'desc': '''Project kind, currently support `exe` and `lib`.
			`exe` for create executable jar target.
			`lib` for create java library.''',
			'default': 'exe'
		},
		{
			'name': 'target_name',
			'desc': 'Project name.',
			'data_type': 'string',
			'default': 'Hello'
		},
		{
			'name': 'sources',
			'desc': 'Scala sources, separated by whitespace.',
			'data_type': 'list',
			'default': ['Hello.scala']
		},
		{
			'name': 'main_class',
			'desc': 'if project kind == `exe` then specify this one for class entry point.',
			'data_type': 'string',
			'default': "Hello"
		},
		{
			'name': 'package',
			'desc': 'Package name, ex: com.mycom.myapp',
			'data_type': 'string',
			'default': None
		}
	]
	
	def __init__(self, out_dir, kind="exe", target_name="Hello.jar", sources=["Hello.scala"], main_class="Hello", package=None):
		super(ScalaGenerator, self).__init__(out_dir)
		
		if kind == "exe":
			self._build_file = "build.xml"
		
		if not self._build_file:
			raise GeneratorException, "Unsupported kind `%s`" % kind
		
		if kind not in ['exe', 'lib']:
			raise GeneratorException, "Invalid kind, only support: `exe` and `lib`." 
		
		self.kind = kind
		self.target_name = target_name
		self.main_class = main_class.title()
		self.package = package
		
		if isinstance(sources, (str, unicode)):
			sources = sources.split(" ")
		
		self.sources = sources
		self._template_build = Template('''
<project default="run" name="$main_class">
	<property name="project.dir" value="." />
	<property name="main.class" value="$main_class_with_package" />
	<property name="scala.home" value="$scala_home" />
	<property name="build.dir" value="$${project.dir}/build" />
	<property name="source.dir" value="$${project.dir}/src" />
	
    <target name="init">
    	
    	<!-- scala libraries for classpath definitions -->
    	<property name="scala-library.jar" value="$${scala.home}/lib/scala-library.jar" />
    	<property name="scala-compiler.jar" value="$${scala.home}/lib/scala-compiler.jar" />
    	
        <!-- classpath for the compiler task definition -->
        <path id="scala.classpath">
          <pathelement location="$${scala-compiler.jar}" />
          <pathelement location="$${scala-library.jar}" />
        </path>

        <!-- classpath for project build -->
    	<path id="build.classpath">
    		<pathelement location="$${scala-library.jar}"/>
    		<fileset dir="$${project.dir}/lib">
    			<include name="*.jar"/>
			</fileset>
    		<pathelement location="$${build.dir}/classes" />
    	</path>
    	
    	<taskdef resource="scala/tools/ant/antlib.xml">
	      <classpath refid="scala.classpath" />
	    </taskdef>
    	
    	<mkdir dir="$${build.dir}" />
    	<mkdir dir="$${source.dir}" />
    	<mkdir dir="$${project.dir}/lib" />

    </target>

    <target name="build" depends="init" description="Build class">
        <mkdir dir="$${build.dir}/classes" />
    	<scalac classpathref="build.classpath" deprecation="on"
    	       destdir="$${build.dir}/classes"
    	       force="never" srcdir="$${source.dir}">
    	      <include name="**/*.scala">
    	    </include>
    	</scalac>
    </target>

	
	  <!-- delete compiled files -->
	  <target description="clean" name="clean">
		<delete includeemptydirs="true">
	  		<fileset dir="$${build.dir}" />
	  	</delete>
	    <delete dir="$${project.dir}/doc" />
	  </target>
	
	  <!-- run program -->
	  <target depends="build" description="run" name="run">
	    <java classname="$${main.class}" classpathref="build.classpath" />
	  </target>
	
	<!-- ================================= 
          target: $target_name              
         ================================= -->
    <target name="$target_name" depends="build" description="Create $target_name file">
        <mkdir dir="$${build.dir}/jar" />
    	<copy file="$${scala-library.jar}" todir="$${project.dir}/lib/" />
    	<path id="jar.class.path">
    		<fileset dir="$${project.dir}">
    			<include name="lib/**/*.jar" />
    		</fileset>
    	</path>
    	<pathconvert dirsep="/" pathsep=" " property="jar.classpath">
    	      <path refid="jar.class.path"></path>
    	      <map from="$${basedir}$${file.separator}lib" to="lib" />
    	</pathconvert>
    	<jar basedir="$${build.dir}/classes" destfile="$${build.dir}/jar/$${ant.project.name}.jar">
    		<zipgroupfileset dir="$${project.dir}/lib" includes="*.jar" />
    		<manifest>
    			<attribute name="Main-Class" value="$${main.class}" />
    			<attribute name="Class-Path" value="$${jar.classpath}" />
    		</manifest>
    	</jar>
    </target>

</project>
		'''.strip() + "\n")
		
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
		#build_file = super(ScalaGenerator, self).generate()
		
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
				'/opt/lib/scala'
			]
			
			for dir in dirs:
				if os.path.exists(dir + "/lib/scala-library.jar"):
					self.scala_home = dir
					break
		
		self.test()

		main_class_with_package = self.main_class
		
		if self.package:
			main_class_with_package = self.package + "." + self.main_class

		f = open(self._build_file, "w")
		data = {
			'target_name': self.target_name,
			'package': self.package and self.package or '',
			'main_class': self.main_class,
			'scala_home': self.scala_home,
			'main_class_with_package': main_class_with_package
		}
		f.write(self._template_build.substitute(**data))
		f.close()
		
		self.build_main_file()
		
		return True
	
	def build_main_file(self):
		paths = [self._normalize_path(self.out_dir), "src"]
		
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

	def rollback(self):
		build_file = os.path.join(self._normalize_path(self.out_dir), self.__build_file)
		
		if os.path.exists(build_file):
			os.unlink(build_file)
		
		
	def test(self):
		if self.kind not in ['exe', 'lib']:
			raise GeneratorException, "Invalid kind, only support: `cmd` and `pkg`."
		
		if isinstance(self.sources, (tuple, list)) == False:
			raise GeneratorException, "Invalid sources type, should be tuple or list"
	
		if not self.scala_home:
			raise GeneratorException, "Cannot get scala_home, please set it manually by exporting to SCALA_HOME environment"
		
		if os.path.exists(self.scala_home) == False:
			raise GeneratorException, "Scala home not exists `%s`" % self.scala_home
		
		if self.kind == "exe" and not self.main_class:
			raise GeneratorException, "Scala kind `exe` should have main_class, please set it with main_class parameter."

		return True
		
	@staticmethod
	def usage():
		parameters = IGenerator.get_help_parameters(ScalaGenerator)
		
		usage_text = '''
Generate Scala project

Parameters:

	%(parameters)s

Examples:

	$ progen -p Scala -o ./hello kind=exe target_name=hello.jar sources="Hello.scala" main_class="Hello"
''' % dict(parameters=parameters)
		return usage_text

	



