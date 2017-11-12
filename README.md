# AutoDependencyInferer
A script which computes the dependency graph for c/c++ files. This dependency graph can then be converted to a bazel config.
This was mostly done as a proof of concept to show that automatic conversion of a reasonably complex project can be automated.
All of the C++ code is nonsense and is only used to get a c++ project to test the dependency graph on.

# Code quality
The code quality for the python part is reasonably poor. Some of it is since the project was just a proof of concept. A refactorization would be needed if the project would continue. The project started out as an playground for the output of the terminal command "nm", therefore a lot of code could be removed which relates to this.

# Features
- Can generate bazel project
- Can handle circular dependencies
- Can handle source files in multiple different folders
- Can give informative comments about missing headers and included but unused headers

# non-features
- Requires that up to date .o files are available
    - only used for finding out which files should be converted to executables instead of libs
- Includes are only allowed relative to the current file
- Can not handle circular dependencies spanning different directories (?)
- Two files can not have the same name eg. /src/foo/include.hpp and src/bar/include.hpp would cause a conflict
- If two .hpp and .cpp have matching names they are assumed to be related
- A lot of hard coded paths are used
- Code is analyzed by stupid text parsing rather than text -> lexemes -> cfg

# Support
I consider this project finished, although a lot of more features could be added. If you want to use it for anything and want support you can mail me

# Licence
This is released under MIT license
