from pbcore.io import SubreadSet,Filters,FastaReader
import sys

def main(parser):
    args = parser.parse_args()

    filt  = Filters()
    dset  = SubreadSet(args.inXml)
    names = nameGen(args.inFile,
                    fileType='list' if args.list else 'fasta')
    if args.subreads:
        filt.addRequirement(QNAME=[('=',name) for name in names])
    else:
        assert len(dset.movieIds) == 1, 'This method olny works for single-movie subreadsets.  use --subreads option for mutli-movie subreadsets'
        filt.addRequirement(zm=[('=',hn) for hn in set(map(getZmw,names))])
    dset.addFilters(filt)
    dset.write(args.outXml)

def nameGen(inFile,fileType='fasta'):
    if fileType=='fasta':
        for rec in FastaReader(inFile):
            yield rec.name
    if fileType=='list':
        #assumes text file where each line starts with 
        #<movie>/<holenumber>/[qstart_qend]
        #e.g. blasr output, no header
        for rec in inFile.read().split('\n'):
            if not rec:
                continue
            #return first three '/'-sep fields
            yield '/'.join(rec.split('/')[:3])

def getZmw(name):
    return int(name.split('/')[1])

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(prog='datasetWhitelist.py', description='Generate a whitelisted dataset xml from an input fasta of reads (subreads or ccs) or file of readnames (e.g. blasr)')
    parser.add_argument('inXml', metavar='inXml', type=str,
                    help='input pacbio subread dataset.')
    parser.add_argument('inFile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help='file with read names (e.g. fasta,blasr output,text file of names). default stdin')
    parser.add_argument('-o,--outXml', dest='outXml', type=str, required=True,
                    help='output xml.' )
    parser.add_argument('-s,--subreads', dest='subreads', action='store_true', default=False,
                    help='whitelist subread names instead of zmws (will only work with subread names, not ccs names).  default false.')
    parser.add_argument('-l,--list', dest='list', action='store_true',  default=False,
                    help='input names as text list.  default false.')

    main(parser)
