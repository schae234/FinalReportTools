#!/usr/bin/python

from __future__ import print_function
from collections import defaultdict
import re
import sys


class process():
    def __init__(self):
        self.final_report = None
        self.map = None
    

class FinalReport(object):

    def __init__(self):
        self.logFile = sys.stdout
        self.delim = "\t"       # how is file delimited?
        self.header = {}        # dict of header info
        self.data_cols = []     # what columns are in file
        self.map = Map()        # map file associated with Report
        self.data = defaultdict(dict)         # huge data store
        self.process_func = self.process_header # process function
        self.allele = "Forward"

        self.SNPs = set()
        self.indiv = set()

    def log(self,*args):
        print(*args,file=self.logFile)
  
    # Method to read in a Final Report file 
    def read_report(self, report):
        with open(report,'r') as file:
            # Read the file in and process the line based on what section you are in 
            # In
            for line_num,line in enumerate(file):
                if line_num % 1000 == 0:
                    self.log("On line {}".format(line_num))
                line = line.strip()
                if line == '[Header]':
                    self.process_func = self.process_header
                elif line == '[Data]':
                    self.process_func = self.process_data
                else:
                    self.process_func(line)

    def read_map(self, map_file):
        self.map = Map()
        self.map.read_map(map_file)

    # Method to process FinalReport Header information
    def process_header(self, line):
        key,val = re.split(r"{}+".format(self.delim),line)
        self.header[key] = val

    # Method to process FinalReport Data Information
    def process_data(self, line):
        fields = line.split(self.delim)
        if not self.data_cols: 
            self.data_cols = fields
            self.ID_col = self.which_data_col("Sample ID")[0]
            self.SNP_col = self.which_data_col("SNP")[0]
            self.a1_col = self.which_data_col(self.allele)[0]
            self.a2_col = self.which_data_col(self.allele)[1]
        else:
            # Extract the data
            ID = fields[self.ID_col]
            SNP = fields[self.SNP_col]
            allele1 = fields[self.a1_col]
            allele2 = fields[self.a2_col]
            # Store it in a data structure
            self.data[ID][SNP] = (allele1,allele2) 
            self.SNPs.add(SNP)
            self.indiv.add(ID)

    def write_ped(self,output_name):
        return 1
    def write_map(self,output_name):
         with open(output_name,'w') as output:
            output.write(str(self.map))

    def which_data_col(self,col_string):
        ''' return a list of data column indices which include the col_string '''
        return [i for i,val in enumerate(self.data_cols) if col_string in val]



class Snp(object):
    def __init__(self, chrom, name, cm, pos):
        self.chrom = chrom
        self.name = name
        self.cm = cm
        self.pos = pos

    @property
    def position_tag(self):
        return "chr%s.%s" % (self.chrom, self.pos)

    def __str__(self, bypos=False):
        return "{}\t{}\t{}\t{}".format(self.chrom, self.position_tag, self.cm, self.pos)

class Map(object):
    def __init__(self):
        self.snp_map = {}
        self.pos_map = defaultdict(dict)
        self.names = []

    def read_map(self,file_name):
        with open(file_name, 'r') as file:
            for line in file:
                chrom,name,cm,pos = line.split()
                # store by name
                snp = Snp(chrom,name,cm,pos)
                self.snp_map[name] = snp
                self.names.append(name)
                # Also store by position
                self.pos_map[str(chrom)][str(pos)] = snp
        self.names.sort()
    
    def add_snp(self, Snp):
        self.snp_mapping[snp.name] = Snp

    def __str__(self, bypos = False):
        full_map = ''
        for name,snp in self.snp_map.iteritems():
            full_map = full_map + str(snp) + "\n"
        return full_map

class Ped(object):
    def __init__(self):
        self.individuals = defaultdict(Individual)
        self.snp_map = Map()

    def add_individual(self, fam, name, sex, pheno):
        self.individuals[name] = Individual(fam,name,sex,pheno)


class Individual(object):
    def __init__(self, fam, name, sex, pheno):
        self.fam = fam,
        self.name = name,
        self.sex = sex,
        self.pheno = pheno
        self.genotypes = defaultdict(dict)




