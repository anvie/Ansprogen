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


class GolangGenerator(IGenerator):	
	
	name = "Golang"
	source_ext = ".go"
	parameters = [
		{
			'name': 'kind',
			'data_type': 'string',
			'desc': '''Project kind, can be `cmd` or `pkg`.
		`cmd` for create executable project,
		`pkg` for create package / go lib.''',
			'default': 'cmd'
		},
		{
			'name': 'target_name',
			'data_type': 'string',
			'desc': 'Output target file name',
			'default': 'hello'
		},
		{
			'name': 'sources',
			'data_type': 'list',
			'desc': 'Golang sources, separated by whitespace.',
			'default': ["hello.go"]
		}
	]

	
	def __init__(self, out_dir, kind="cmd", target_name="hello", sources=["hello.go"]):
		super(GolangGenerator, self).__init__(out_dir)
		self._build_file = "Makefile"
		
		if kind not in ['cmd', 'pkg']:
			raise GeneratorException, "Invalid kind, only support: `cmd` and `pkg`." 
		
		self.kind = kind
		self.target_name = target_name
		
		if isinstance(sources, (unicode, str)):
			sources = sources.split(" ")
		
		self.sources = sources
		self._template = Template('''
include $$(GOROOT)/src/Make.inc

TARG=$target_name
DEPS=

GOFILES=$sources

include $$(GOROOT)/src/Make.$kind
		'''.strip() + "\n")
		self._template_main = Template('''
package main

import (
	"fmt"
)

func main() {
	fmt.Println("Yo World!")
}
'''.strip() + "\n")
	
	def generate(self):
		build_file = super(GolangGenerator, self).generate()
	
		self.test()

		f = open(build_file, "w")
		data = {
			'target_name': self.target_name,
			'sources': " ".join(self.sources),
			'kind': self.kind
		}
		#from dbgp.client import brk; brk()
		f.write(self._template.substitute(**data))
		f.close()
		
		main_file = os.path.join(self._normalize_path(self.out_dir), self.target_name)
		
		main_file = self._normalize_source_name(main_file)
		
		f = open(main_file, "w")
		f.write(self._template_main.substitute())
		f.close()
		
		return True
	

	def rollback(self):
		build_file = os.path.join(self._normalize_path(self.out_dir), self.__build_file)
		
		if os.path.exists(build_file):
			os.unlink(build_file)
		
		
	def test(self):
		if self.kind not in ['cmd', 'pkg']:
			raise GeneratorException, "Invalid kind, only support: `cmd` and `pkg`."
		
		if isinstance(self.sources, (tuple, list)) == False:
			raise GeneratorException, "Invalid sources type, should be tuple or list"

		return True


	@staticmethod
	def usage():
		parameters = IGenerator.get_help_parameters(GolangGenerator)
		
		usage_text = '''
Generate Golang project.

Parameters:
	
	%(parameters)s
	
Examples:
	
	$ progen -p Golang -o ./ kind=cmd target_name=hello sources="hello.go"
	
''' % dict(parameters=parameters)
	
		return usage_text
		
	

	



