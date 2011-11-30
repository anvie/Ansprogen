Ansvia Project Generator (Ansprogen)
======================================

Tools for easily create project for any language, currently support for Go and Scala.
But you can extend easily to support other language by extending IGenerator on `ansprogen/generators` dir.

Example Usage
---------------

Create a Go project:

	$ progen -p Golang -o ./hello

Testing:

	$ cd hello/
	$ ls
	  Makefile	hello.go
	$ make
	  6g  -o _go_.6 hello.go
	  6l  -o hello _go_.6
	$ ./hello
	  Yo World!

Create a Scala project:

	$ progen -p Scala -o hello

Testing, create jar and execute using `java -jar`:

	$ cd hello/
	$ ls
	  build.xml	src
	$ ant Hello.jar
	  Buildfile: /Users/Robin/Development/ansvia/project.generator/hello/build.xml

	  init:
	      [mkdir] Created dir: /Users/Robin/Development/ansvia/project.generator/hello/build
	      [mkdir] Created dir: /Users/Robin/Development/ansvia/project.generator/hello/lib

	  build:
	      [mkdir] Created dir: /Users/Robin/Development/ansvia/project.generator/hello/build/classes
	     [scalac] Compiling 1 source file to /Users/Robin/Development/ansvia/project.generator/hello/build/classes

  	Hello.jar:
	      [mkdir] Created dir: /Users/Robin/Development/ansvia/project.generator/hello/build/jar
	       [copy] Copying 1 file to /Users/Robin/Development/ansvia/project.generator/hello/lib
	        [jar] Building jar: /Users/Robin/Development/ansvia/project.generator/hello/build/jar/Hello.jar

	  BUILD SUCCESSFUL
	  Total time: 29 seconds
	$ java -jar build/jar/Hello.jar 
	    Yo World!

More specific:

	$ progen -p Golang -o /tmp/hello kind=cmd target_name=hello sources=hello.go

Or use interactive mode:

	$ progen -p Golang -i
	Creating Golang project
	Interactive mode.
	 -> out_dir: ./hello
	 -> kind: cmd
	 -> target_name: hello
	 -> sources: hello.go

Every language has the specific options, if you want to know what the supported options just type `help` followed by project name,
for example:

	$ progen help Scala

Will show project spec details:

	Generate Scala project

	Parameters:

		kind -- Project kind, currently support `exe` and `lib`.
				`exe` for create executable jar target.
				`lib` for create java library.
		target_name -- Target output name.
		sources -- scala sources, separated by whitespace.
		main_class -- if project kind == `exe` then specify this one
					for class entry point.
		package -- Package name, ex: com.ansvia.myapp.

	Examples:

		$ progen -p Scala -o ./hello kind=exe target_name=hello.jar sources="Hello.scala" main_class="Hello"


Show all supported projects:

	$ progen -t
	
	Ansprogen 0.0.3
	
	Supported generators:
	
	* Golang
	  `help Golang` to show Golang's project spec details
	
	* Scala
	  `help Scala` to show Scala's project spec details
	
	* Scala:sbt
	  `help Scala:sbt` to show Scala:sbt's project spec details

Create Scala project with sbt tools:

	$ progen -p Scala:sbt -o ~/hello_sbt

Installation
-------------

Using `easy_install`:

    $ easy_install ansprogen

Using `pip`:

	$ pip install ansprogen
	
Source code
-------------

Fork me on github: https://github.com/anvie/Ansprogen

Enhancement and new language support are welcome feel free to Fork and gime pull request.


