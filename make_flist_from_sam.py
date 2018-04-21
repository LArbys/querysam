import os,sys,re,json
from operator import itemgetter

# we read in a list of files
# for each file, we query sam and get
#  (1) run, subrun
#  (2) number of events
# Save into a json file


def get_sam_metadata( flisttxt, output_text, output_indexed, badlist ):
    #flisttxt = "flist_larcv.txt"
    #output_text = "metadata_larcv.json"
    #output_indexed = "indexed_meta_larcv.json"

    flist = open( flisttxt, 'r' )
    fnames = flist.readlines()
    flist.close()
    
    nfiles = len(fnames)
    print "Number of files: ",nfiles

    filedict = {}
    eventsub = {}
    
    badfiles = open(badlist,'w')

    nprocessed = 0
    for f in fnames:
        f = f.strip()
        cmd = "samweb get-metadata --json %s"%(f)
        try:
            psam = os.popen(cmd)
            lsam = psam.read()
            jsam = json.loads(lsam)
        except:
            print "COULD NOT PROCESS: ",f
            print >> badfiles,f
            continue

        nevents = 0
        if 'event_count' in jsam:
            nevents = jsam['event_count']
        runlist = jsam['runs']
        if len(runlist[0])>=3:
            for i in runlist:
                x = i.pop()
        try:
            runlist = sorted(runlist, key=itemgetter(0,1))
        except:
            print "WHAT?",runlist
            sys.exit(-1)
        filedict[ f ] = {"run":runlist[0][0],"subrun":runlist[0][1],"listruns":runlist,"event_count":nevents}
        eventsub[ "%06d.%06d" % (runlist[0][0], runlist[0][1]) ] = {"run":runlist[0][0],"subrun":runlist[0][1],"listruns":runlist,"event_count":nevents}
        #print f
    
        with open(output_text,'w') as out:
            json.dump( filedict, out, sort_keys=True, indent=2 )

        with open(output_indexed,'w') as out:
            json.dump( eventsub, out, sort_keys=True, indent=2 )

        nprocessed+=1
        if nprocessed%100==0:
            print "Finished ",nprocessed," of ",nfiles
    badfiles.close()


if __name__=="__main__":

    # larcv
    #get_sam_metadata( "flist_larcv.txt", "metadata_larcv.json", "indexed_meta_larcv.json", "badmeta_larcv.txt" )

    # larlite opreco
    #get_sam_metadata( "flist_opreco.txt", "metadata_opreco.json", "indexed_meta_opreco.json", "badmeta_opreco.txt" )

    # larlite reco2d
    get_sam_metadata( "flist_reco2d.txt", "metadata_reco2d.json", "indexed_meta_reco2d.json", "badmeta_reco2d.txt" )

