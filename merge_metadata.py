import os,json,time

def merge_metadata( larcvjson, oprecojson, reco2djson,
                    larcvindex, oprecoindex, reco2dindex,
                    mctruthjson=None, mctruthindex=None ):
    """ we merge meta data for each type of file"""

    start = time.time()
    print "Start of meta-data merger"
    
    # meta data files
    meta = {}
    meta["larcv"] = json.load(open(larcvjson,'r'))
    meta["opreco"] = json.load(open(oprecojson,'r'))
    meta["reco2d"] = json.load(open(reco2djson,'r'))
    if mctruthjson is not None:
        meta["mctruth"] = json.load(open(mctruthjson,'r'))
    else:
        meta["mctruth"] = None

    # index files
    index = {}
    index["larcv"] = json.load(open(larcvindex,'r'))
    index["opreco"] = json.load(open(oprecoindex,'r'))
    index["reco2d"] = json.load(open(reco2dindex,'r'))
    if mctruthjson is not None:
        meta["mctruth"] = json.load(open(larcvjson,'r'))
    else:
        meta["mctruth"] = None
        
    ikeys = index["larcv"].keys()
    print "number of indices: ",len(ikeys)
    print ikeys[0]

    # match oto larv index
    for f in ["larcv","opreco","reco2d"]:
        m = meta[f]
        for fname in m:
            run  = m[fname]["run"]
            subrun = m[fname]["subrun"]
            k ="%06d.%06d"%(run,subrun)

            if k not in ikeys:
                continue
            index["larcv"][k][f+"-file"] = fname

    completed = 0
    for k in ikeys:
        allfound = True
        for f in ["larcv","opreco","reco2d"]:
            if f+"-file" not in index["larcv"][k]:
                allfound = False
                break
        if allfound:
            completed += 1

    print "Number of merges completed: ",completed
    end = time.time()
    print "Elapsed time: ",end-start

    out = open( "merged_indexed_metadata.json", 'w' )
    json.dump(index["larcv"], out )
    print "Saved."

    return None


if __name__ == "__main__":

    merge_metadata( "metadata_larcv.json", "metadata_opreco.json", "metadata_reco2d.json",
                    "indexed_meta_larcv.json", "indexed_meta_opreco.json", "indexed_meta_reco2d.json" )
    
