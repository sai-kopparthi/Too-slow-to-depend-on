# Too-slow-to-depend-on

When dependencies get updated software devs must balance between including the new functionalities, but risk things breaking, or sticking with the tried and true, but missing out on the new cool features. Technical lag measures how far a package is behind the most current dependency versions. In the paper An Empirical Analysis of Technical Lag in npm Package Dependencies, Zeroualli et al. study technical lag in npm packages and reasons for it.

Inspired by Zeroualli et al.’s paper, here we will study a simplified version of technical lag on a subset of 1,000 npm projects. npm packages often depend on other packages, which must be listed as “dependencies”, “devDependencies”, “peerDependencies”, etc., in their code’s package.json file, as per npmjs’s documentation.

In a set of 1,000 npm packages, there may be two or more packages that depend on different versions of the same dependency. E.g., package P1 may depend on “rimraf” version 2.1.3, while another package, P2, on a newer, “rimraf” version 2.5.1. In general, for a dependency “foo” denote by Time_set(npm1000commits, foo) the time of the first (i.e., oldest) commit, among all commits in the 1,000 npm projects, which introduced the most recent version of “foo” in any package of that set. Thus, in the above “rimraf” example, the date of the first commit of the “rimraf” 2.5.1 introduction would be that earliest date.

Next, for any package “bar” having “foo” as a dependency, denote by Time_package(foo,bar) the time of the first (i.e., oldest) commit introducing the most recent version of “foo” in “bar”. Then, the technical lag of dependency “foo” in package “bar” is

TLag(foo, bar) = Time_set(npm1000commits, foo) - Time_package(foo, bar).

The technical lag of a package “bar” TLag(bar), will be the maximum of the lags of all dependencies in it. Thus, in the above “rimraf” example, P2 will have a zero time lag, and P1 will have some non-zero time lag.

 A pythonscript using the r2c platform to identify the top 10 laggiest packages, among a set of 1,000 npm packages
