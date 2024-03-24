
#!/bin/bash

# generates 10 random input files and compiles the output files
# this test is run to ensure no exceptions can occur with because of the input

for i in {1..5}
do
    python3 src/create_files.py
    python3 src/test.py
    echo $i" was run without exception"
done

echo ""
echo "  TESTING COMPLETE"
echo ""