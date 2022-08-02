Refmeter, measurable refactoring metrics tool
=============================================
Written in python, ironically does not work for python code.

### Dependencies
pathlib, os, sys

### Usage
```
    ./refmeter.py path [sortColumnNumber]
    example:
    ./refmeter.py
    ./refmeter.py . 1  <- sort by first column, which is line count, default is 5
    columns:
    1 - line count per file
    2 - code blocks count ( what is inside {} )
    3 - parameter blocks count (what is inside () )
    4 - 'case' operator per file ( as for it indicates code block, but does not wrapped in {} )
    5 - max nest level per file (   {} is 1, { {} } is 2  ) <- default
        if() { // nest level 1
            if() { // nest level 2
                    if() { // nest level 3
                    }
                }
            }
```
## How it works
Refmeter does not analyze any specific code patterns, instead it rely on code blocks, basically counting bracets.

### Example analysys
#### Long switch case antipattern
will be detected by counting 'case' keyword
#### Multiple nested if antipattern
```
    if() {
        if() {
            if() {
                ...
            }
        }
    }
```
will be detected by max nested level (5 column)
#### Long class antipattern
will be detected by couting lines per file

### General rule
Keep all parameters as low as possible
