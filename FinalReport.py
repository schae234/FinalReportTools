#!/usr/bin/python

import re
from collections import defaultdict

class FinalReport:

    def __init__(self):
        self.delim = "\t"       # how is file delimited?
        self.header = {}        # dict of header info
        self.data_cols = []     # what columns are in file
        self.map = Map()        # map file associated with Report
        self.data = defaultdict(dict)           # huge data store
        self.process_func = self.process_header # process function
  
    # Method to read in a Final Report file 
    def read_report(self, finalReport_txt):
        with open(finalReport_txt,'r') as f:
            # Read the file in and 
            while f.readable():
                line = f.readline().strip()
                if line == '[Header]':
                    self.process_func = self.process_header
                elif line == '[Data]':
                    self.data_cols  = f.readline().strip().split(self.delim)
                    self.process_func = self.process_data
                else:
                    self.process_func(line)

    # Method to process FinalReport Header information
    def process_header(self, line):
        delim = re.compile(r'\t+')
        key,val = delim.split(line)
        self.header[key] = val

    # Method to process FinalReport Data Information
    def process_data(self, line):
        snp,ind,f1,f2,t1,t2,ab1,ab2,gc,x,y = line.split(self.delim)
        self.data[ind][snp] = {
            'gc' : gc,
            'x' : x,
            'y' : y,
            'alleles' : {
                'top' : [t1,t2],
                'forward' : [f1,f2],
                'ab' : [ab1,ab2],
            },
        }

    def print_ped(self):
        return 1
    def print_map(self):
        return 1 


class Snp:
    def __init__(self, chrom, name, cm, pos):
        self.chrom = chrom
        self.name = name
        self.cm = cm
        self.pos = pos

    @property
    def position_tag(self):
        return "chr%s.%s" % (self.chrom, self.pos)

    def __str__(self, bypos=False):
        return "%s\t%s\t%s\t%s" % (self.chrom, self.position_tag, self.cm, self.pos)

class Map:
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
        self.snp_mapping[snp.name] = snp

    def __str__(self, bypos = False):
        full_map = ''
        for name,snp in self.snp_map.iteritems():
            full_map = full_map + str(snp) + "\n"
        return full_map

class Ped:
    def __init__(self):
        self.individuals = defaultdict(Individual)
        self.snp_map = Map()

    def add_individual(self, fam, name, sex, pheno):
        self.individuals[name] = Individual(fam,name,sex,pheno)


class Individual:
    def __init__(self, fam, name, sex, pheno):
        self.fam = fam,
        self.name = name,
        self.sex = sex,
        self.pheno = pheno
        self.genotypes = defaultdict(dict)




