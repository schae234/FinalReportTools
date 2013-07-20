#!/usr/bin/python

class FinalReport:

    def __init__(self):
        self.map = Map()


class Snp:
    def __init__(self, chrom, name, cm, pos):
        self.chrom = chrom
        self.name = name
        self.cm = cm
        self.pos = pos

    def mccue_name():
        return "chr%s.%s" % (self.chrom, self.pos)

class Map:
    def __init__(self):
        self.snp_map = {}

    def read_map(self,file_name):
        with open(file_name, 'r') as file:
            for line in file:
                chrom,snp,cm,pos = line.split()
                self.snp_mapping[snp] = Snp(chrom,name,cm,pos)
