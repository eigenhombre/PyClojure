# PyClojure

This project consists of the first steps of an implementation of
the Clojure language in Python.  At the moment it is merely interpreted
and is incomplete (see file test_lisp.py for examples). 

**Note**: the [clojure-py](http://github.com/halgari/clojure-py) project is much further along at this point; however, 
I'm keeping this code around as an example of using the Ply tools.

#### What works:

- REPL with history and readline support
- Parsing and storage of trees of lists, vectors, atoms, integers, floats
- 'def' and simple evaluation
- A few builtin functions and access to functions in Python's main namespace
- setup.py packaging

## Dependencies

- [PLY](http://www.dabeaz.com/ply/), for lexing and parsing. It turns
  out Python is actually quite serviceable for writing compilers,
  particularly for prototyping -- one of the reasons for this project
  was to see how far I could push this.
- [Nose](http://readthedocs.org/docs/nose/en/latest/), to run unit tests.
- Python 2.6+

## Why Clojure-in-Python?

The long JVM startup time makes use of Clojure for scripting common
system tasks somewhat unworkable, or at least irritating.
[NewLISP](http://www.newlisp.org/) would be an option, but Clojure is
such a nice Lisp; this particular implementation is meant to
eventually be syntax-compatible with Clojure (as currently implemented
on the JVM). The goal is to provide a real Lisp with macros, and
Clojure's syntactic goodness, as well as immutable data structures,
which can coexist with Python and make use of its extensive,
'batteries included' libraries.

There has been [some
discussion](http://groups.google.com/group/clojure/browse_thread/thread/d910983a4c9ed3f5)
as well about getting Clojure running under PyPy, something which I
think would be quite interesting.

Feel free to join in!  For next steps, see Issues list on GitHub.
Please see the file guidelines.txt for contribution guidelines.

## Author

Primary contact: John Jacobsen, NPX Designs, Inc. john@mail.npxdesigns.com
(See AUTHORS file for complete list of contributors)
