#!/usr/bin/env python3
import sys
from optparse import OptionParser
from collections import defaultdict


if sys.version_info[0] != 3:
	raise Exception("Python must be version 3")


def main(args):
    parser = OptionParser()
    parser.add_option("--snp_info",type=str,help="This input file contains the columns necessary to make a map file.")
    parser.add_option("--final_report",type=str,help="This input file contains the columns necessary to make a ped file.")
    parser.add_option("--output_name",type=str,help="This will be the name of your output files.")
    #parser.add_option("--seperator",type=str,default="\t",help="Columns in the input files are seperated by this character (default is tab)")
    options,args = parser.parse_args()

    if not options.snp_info:
        parser.print_help()
        sys.exit("You need to specify an SNP info file using --snp_info option, see the help above")
    if not options.final_report:
        parser.print_help()
        sys.exit("You need to specify an Final Report file using --final_report option, see the help above")
    if not options.output_name:
        parser.print_help()
        sys.exit("You need to specify an OutPut Name using --output_name option, see the help above")

    # Do the Map Calculations
    with open(options.snp_info,'r') as f:
        clear()
        header("SNP Info")
        headers = []
        for i in range(1,11):
            line = f.readline().strip()
            print("(Line " + str(i) + ") |\t"+ "\t".join(line.split('\t')))
            headers.append(line)
        skip   = int(input("Which line is the header line (0 for none)?:   "))
        clear()
        header("HEADER Columns")
        for i,l in enumerate(headers[skip-1].split('\t')):
            print("(Line {}) |\t{}".format(i+1,l))
        id  = int(input("Which Row is the ID column?          "))-1
        chr = int(input("Which Row is the Chromosome column?  "))-1
        pos = int(input("Which Row is the position column?    "))-1
    clear()
    header("Generating Map File....")
    snps     = defaultdict(list)
    chroms   = set()
    with open(options.snp_info,'r') as IN:
        # Skip header lines
        for i in range(0,skip):
            line = IN.readline().strip()
        # Create the rest of the map file
        for line in IN:
            flds = line.strip().split('\t')
            snps[flds[id]] = [flds[chr],flds[id],'0',flds[pos]]
            # We dont want to mess up the chromosome field
            chroms.add(flds[chr])
        # print out stats:
        print("Processed {} unique SNPs:".format(len(snps)))
        print("Processed the following Chromosomes\n\t{}".format(",".join(chroms)))
        header("Done")
        input("Look right? Press Enter to Continue")
    # Print out the map file
    header("Saving Map File....")
    ordered_snps = list(snps.keys())
    ordered_snps.sort()
    with open(options.output_name+".map",'w') as OUT:
        for snp in ordered_snps:
            print("\t".join(snps[snp]),file=OUT)
    header('Done')


    # Do the PED Calculations
    with open(options.final_report,'r') as IN:
        clear()
        header("FINAL REPORT")
        headers = []
        for i in range(1,31):
            line = IN.readline().strip()
            print("Line " + str(i) + "\t|  " + "\t".join(line.split('\t'))[:80])
            headers.append(line)
        skip   = int(input("Which line is the header line (0 for none)?:    "))
        clear() 
        header("Header Columns:")
        for i,l in enumerate(headers[skip-1].split('\t')):
            print("(Line {}) |\t{}".format(i+1,l))
        id  = int(input("Which Line is the Individual ID column?   "))-1
        snp = int(input("Which Line is the SNP ID Column           "))-1
        a1  = int(input("Which Line is the Allele 1 Column?        "))-1
        a2  = int(input("Which Line is the Allele 2 Column?        "))-1
        famid =   input("What do you want the Fam Id to be?        ").strip()
        altr  =   input("Recode alleles to numeric? [Y/N]          ")

    if altr.upper() == 'Y':
        old = "-ACGT"
        new = "01234"
    else:
        old = '-'
        new = '0'
    transtab = str.maketrans(old,new)
        

    clear()
    header('Processing Final Report...')
    ind = defaultdict(dict)
    with open(options.final_report,'r') as IN:
        for i in range(0,skip):
            line = IN.readline().strip()
        for i,line in enumerate(IN):
            flds = line.strip().split('\t')
            ind[flds[id]][flds[snp]] = "{} {}".format(flds[a1],flds[a2]).translate(transtab)
            if i % 500000 == 0:
                header("......processed {} lines".format(i))
    header("Done")
    print("Processed {} Individuals".format(len(ind)))
    input("Look right? Press enter to Continue")

    clear()
    header("Saving PED FILE....")
    # print out the PED file
    with open(options.output_name+".ped",'w') as OUT:
        for i in ind.keys():
            header("Processing {}".format(i))
            print("{}\t{}\t0\t0\t0\t0".format(famid,i),sep="\t",end="",file=OUT)
            for snp in ordered_snps:
                if snp in ind[i].keys():
                    print("\t"+ind[i][snp],end="",file=OUT)
                else:
                    print("\t0 0",end="",file=OUT)
            print("\n",file=OUT,end="")



def clear():
    print("\n"*1000)

def header(text):
    print("-"*20,text,"-"*20)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
