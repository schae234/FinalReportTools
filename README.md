FinalReportTools
================

Tools to Handle Illumina SNP Final Reports

Final2MapPed
------------

This script takes two files, 1) a map like file and 2) a final report 
and does the appropriate conversions to PLINK map and ped files. Running
the script will bring you through a wizrd which has you select the appropriate
data columms from your files.

```{bash}
Usage: Final2MapPed.py [options]

Options:
  -h, --help            show this help message and exit
  --snp_info=SNP_INFO   This input file contains the columns necessary to make
                        a map file.
  --final_report=FINAL_REPORT
                        This input file contains the columns necessary to make
                        a ped file.
  --output_name=OUTPUT_NAME
                        This will be the name of your output files.
```
