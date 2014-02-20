#!/usr/bin/python3


final_report = "/home/rob/Codes/Gait/Minnesota-McCue_Equine_13jul2013_FinalReport.txt"
map_file = "/home/rob/Codes/Equine_70k.map"

# Read in the map file and put everything in a dictionary
map_data = dict()
FIN = open(map_file,'r')
for line in FIN:
    line = line.strip()
    chrom,id,cm,pos = line.split()
    # We want to be able to look up snps by id later since thats how they 
    # come back in the final report, just store the line because we will
    # just be rearranging by line later
    map_data[id] = line

# Read in the genotype data and put in a dictionary
geno_data = dict()
GENO = open(final_report,'r')
# the final report has a stupid header that is hard to parse. We 
# want to start processing two lines after [Data] so lets keep track
# of if we have seen the [Data] line and how many lines after we are
seen_data = False
lines_after_data = 0
for line in GENO:
    line = line.strip()
    # Are we on data line?
    if seen_data == False and '[Data]' not in line:
        # we must be in the [Header] section
        # print out the line so we know which ones we skip
        print(line)
    elif seen_data == False and '[Data]' in line:
        # we are on the [Data] line, we need to just go one more
        seen_data = True         
        print(line)
    elif seen_data == True and lines_after_data < 1:
        # This takes care of the header line. once lines after data == 1, we're done 
        lines_after_data += 1 
        print(line)
    else:
        snp_id,id,f1,f2,t1,t2,ab1,ab2,gc,x,y = line.split()
        # Once we get here, we need to keep track of things in our dictionary
        # We want to print out things by individual in the ped file so that will be
        # our first level of our dictionary
        if id not in geno_data:
            geno_data[id] = {}
        # Check out what translate is doing here: 
        # http://www.tutorialspoint.com/python/string_translate.htm
        f1 = f1.translate(str.maketrans('-ACGT','01234'))
        f2 = f2.translate(str.maketrans('-ACGT','01234'))
        # The next level of our dictionary will be the snp id, which will point 
        # at the genotype calls for the snp
        geno_data[id][snp_id] = f1+" "+f2

        # at the end out geno_data will look something like:
        # { 'CAN1' : {
        #       'BIEC1' : "T A",
        #       'BIEC2' : "G C",
        #       ....
        #   },
        #   'CAN2' : {
        #       'BIEC2' : "G G",
        #       'BIEC3' : "A A",
        #       ...
        #   }
        #   ...
        # }

# Now we want to print our the ped file
PED = open("OUTPED.ped",'w')
# it has a line per individual:
for ind in geno_data.keys():
    # we want to print our the first couple of columns
    # Which are: fam,ind.father,mother,sex,status
    # Check out what the format ftring method does here:
    # http://docs.python.org/3/library/string.html#string-formatting
    print("FAM\t{}\t0\t0\t0\t0".format(ind),file=PED,end="",sep="")
    # now we want to print out every snp genotype for this individual
    snps = list(map_data.keys())
    # We need to sort them
    snps.sort()
    for snp in snps:
        # maybe this ind doesn't have this geno, check this:
        if snp not in geno_data[ind]:
            # If its not in there, assign it as missing
            geno = "0 0"
        else:
            # If it is in there, snatch it up!
            geno = geno_data[ind][snp]
        # print to the ped file with a prepended tab, which will seperate out 
        # out columns
        print("\t{}".format(geno),file=PED,end="",sep="")
    # End with a newline since we have been skipping them:
    print("\n",file=PED,end='')

# Now print out the map file the same way we did the ped file
# since the order of the snps matters
MAP = open("OUTMAP.map",'w')
snps = list(map_data.keys())
snps.sort()
for snp in snps: 
    print(map_data[snp],file=MAP)
 

