cc_library(
name = "tangle#0",
visibility = ["//visibility:public"],
srcs = ["circ1.cpp", "circ2.cpp"],
hdrs = ["circ2.hpp", "circ1.hpp"],
deps = ["//src/folder:banana", ":hippo", ":fruit", ":globals"],
)

cc_binary(
name = "main",
visibility = ["//visibility:public"],
srcs = ["main.cpp"],
deps = ["//src/folder:banana", ":tangle#0", ":hippo"],
)

cc_binary(
name = "main2",
visibility = ["//visibility:public"],
srcs = ["main2.cpp"],
deps = ["//src/folder:banana", ":apple"],
)

cc_library(
name = "unused",
visibility = ["//visibility:public"],
srcs = ["unused.cpp"],
hdrs = ["unused.hpp"],
)

cc_library(
name = "unused2",
visibility = ["//visibility:public"],
srcs = ["unused2.cpp"],
hdrs = [],
deps = [":unused"],
)

cc_library(
name = "apple",
visibility = ["//visibility:public"],
srcs = ["apple.cpp"],
hdrs = ["apple.hpp"],
)

cc_library(
name = "globals",
visibility = ["//visibility:public"],
srcs = [],
hdrs = ["globals.hpp"],
)

cc_library(
name = "hippo",
visibility = ["//visibility:public"],
srcs = [],
hdrs = ["hippo.hpp"],
deps = [":fruit"],
)

cc_library(
name = "fruit",
visibility = ["//visibility:public"],
srcs = ["fruit.cpp"],
hdrs = ["fruit.hpp"],
)

