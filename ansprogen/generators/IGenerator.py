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

class GeneratorException(Exception):
	pass

class IGenerator(object):
	
	name = ""
	source_ext = ""
	usage = ""
	
	def __init__(self, out_dir):
		self.out_dir = out_dir
		self._build_file = None
	
	def generate(self):
		if os.path.isdir(self.out_dir) != True:
			if os.path.isfile(self.out_dir) != True:
				os.makedirs(self.out_dir)
			else:
				raise GeneratorException, "Already exists as file `%s`" % self.out_dir
		
		build_file = os.path.join(self._normalize_path(self.out_dir), self._build_file)
		
		if os.path.exists(build_file):
			print "Build file already exists `%s`" % build_file,
			ui = raw_input("Remove? [y/n] ")
			if ui == "y":
				os.unlink(build_file)
				if os.path.exists(build_file):
					raise GeneratorException, "Build file already exists `%s` (cannot remove)" % build_file
			else:
				return None
		
		return build_file
	
	def set_build_file(self, build_file):
		self.__build_file = build_file
	
	def _normalize_path(self, path):
		rv = path.strip("")
		rv = re.sub("/+$", "", rv)
		return rv
	
	def _normalize_source_name(self, path):
		if path.endswith(self.source_ext):
			return path
		return path + self.source_ext
	
	@staticmethod
	def get_help_parameters(Cls):
		rv = []
		params = Cls.parameters
		for p in params:
			if p.has_key('default') and p['default']:
				rv.append('%s -- {%s} %s, default %s.' % (p['name'], p['data_type'], p['desc'], p['default']))
			else:
				rv.append('%s -- {%s} %s' % (p['name'], p['data_type'], p['desc']))
			
			if p.has_key('accept'):
				rv.append("\tsupport: %s.\n" % ", ".join(p['accept']))
			
		return "\n\t".join(rv)
	
	@staticmethod
	def usage():
		raise GeneratorException, "Not implemented"
	
	def build_main_file(self):
		raise GeneratorException, "Not implemented"

	def rollback(self):
		"""This called when gerenator fail.
		"""
		raise GeneratorException, "Not implemented"

	def __repr__(self):
		return "<Generator[%s]>" % str(self.name)

	def test(self):
		raise GeneratorException, "Not implemented"



