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

from optparse import OptionParser

import sys

from generators import *

VERSION = "0.0.4"

_generators = [
	golang.GolangGenerator,
	scala.ScalaGenerator,
	scala_sbt.ScalaGenerator
]


def get_generator(name):
	for g in _generators:
		if g.name == name:
			return g
	return None

def list_generators():
	for g in _generators:
		print "* " + g.name
		print "  `help %s` to show %s's project spec details" % (g.name, g.name )
		print ""

parser = OptionParser()

parser.add_option("-p", "--project", dest="project", help="Project for. Show supported generators using `-t` parameter.")
parser.add_option("-o", "--out-dir", dest="out_dir", help="Output directory")
parser.add_option("-i", "--interactive", dest="interactive", action="store_true", help="Interactive mode")
parser.add_option("-t", dest="list_generators", action="store_true", help="Show supported generators.")

usage = '''
To get usage details on every supported project,
execute `help` followed by project name, example:

	$ progen help Golang
	
'''

def main():
	
	print "Ansprogen " + VERSION
	
	opts, args = parser.parse_args()
	
	if len(args) == 2:
		opt, proj = args
		if opt == "help":
			gen = get_generator(proj)
			if gen:
				print gen.usage()
				return 0
			else:
				print "Unknown help for project `%s`" % proj
				return 3
	
	if opts.list_generators:
		print ""
		print "Supported generators:\n"
		list_generators()
		return
	
	if not opts.project:
		print "No project name, please specify it with `-p` or `--project`"
		parser.print_help()
		print usage
		return 1

	if not opts.out_dir:
		print "No output dir, please specify it with `-o` or `--out-dir`"
		parser.print_help()
		print usage
		return 1

	if not opts.interactive and not opts.out_dir:
		print "No out dir, please specify it with `-o` or `--out-dir`"
		parser.print_help()
		print usage
		return 1
	
	Generator = get_generator(opts.project)
	
	if not Generator:
		print "Unknown project `%s`" % opts.project
		parser.print_usage()
		print usage
		return 2
	

	params = dict(map(lambda x: x.split("="), args))
	params['out_dir'] = opts.out_dir
	
	#from dbgp.client import brk; brk()
	
	if opts.interactive:
		print "Creating %s project" % Generator.name
		print "Interactive mode."
		i_params = Generator.parameters
		for p in i_params:
			name = p['name']
			
			if p.has_key('desc'):
				print "   " + p['desc']
				
			if p.has_key('accept'):
				accept = p['accept']
				for i, a in enumerate(accept):
					accept[i] = "%d: %s" % ((i+1), a)
				print "   supported: " + ', '.join(accept)
			
			if isinstance(p['default'], (str, unicode)):
				default = p.has_key('default') and p['default'] or ''
			else:
				default = ''
			
			param = raw_input(" -> " + name + ' [' + default + '] ' + ": ")
			
			if len(param.strip()) == 0:
				param = default
			
			params[name] = param
	
	#print params
	
	#from dbgp.client import brk; brk()
	gen = Generator(**params)
	
	rv = gen.generate()
	
	if rv != True:
		gen.rollback()
		return 4
	
	print "Output: `%s`" % opts.out_dir
	print "Done."

	return 0



if __name__ == '__main__':
	sys.exit(main())






