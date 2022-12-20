#!/usr/bin/env python

from collections import namedtuple
import glob
import os
import shutil


def process_one_video( video, subs_folder ):
    lang_dict = {
        "English": "eng"
    }
    subs_found = {}
    
    video_name = os.path.splitext( os.path.basename(video) )[0]
    video_ext = ""
    video_path = os.path.dirname( video )
    for root, subdirs, files in os.walk(subs_folder):
        for d in subdirs:
            if d == video_name:
                video_subs_folder = os.path.join(root, d)
                print( "found video subs folder: " + video_subs_folder )
                for lang_source, lang_target in lang_dict.items():
                    sub_source = ""
                    matching_pattern = os.path.join( glob.escape(video_subs_folder), "*_" + lang_source + ".*" )
                    # print( matching_pattern )
                    # print( glob.glob(matching_pattern))
                    list_of_subs = list(filter( os.path.isfile, glob.glob(matching_pattern ) ))
                    # print( list_of_subs )
                    # Find the file with max size from the list of files
                    sub_source = max( list_of_subs, key =  lambda x: os.stat(x).st_size)
                    # print( "sub found: " + video_name + sub_source )
                    
                    if sub_source:
                        video_ext = os.path.splitext( os.path.basename(sub_source) )[1]
                        sub_target = os.path.join( os.path.dirname( video ), video_name ) + "." + lang_target + video_ext
                        print( "copying: " + sub_source + " to: " + sub_target )
                        shutil.copy2( sub_source, sub_target )
                        subs_found[lang_target] = sub_source
                    else:
                        print( "error: couldn't find sub file for: " + video )
        break    # non-recursive walk
    
    # print( subs_found )
    
    for lang in lang_dict.values():
        if lang not in subs_found:
             print( "error: couldn't find sub file for: " + video )
    

def process_one_folder( folder ):
    print( "processing " + folder )
    subs_folder = os.path.join( folder, "Subs" )
    if os.path.isdir(subs_folder):
        print( "found subs folder" )
    for folders, subfolders, files in os.walk(folder):
        for video in files:
            # print( "video: " + video )
            video_types = [".mkv", "mp4"]
            is_video = False
            for t in video_types:
                if video.endswith(t):
                    is_video = True
            if is_video:
                process_one_video( os.path.join( folder, video ), subs_folder )
        break       # non-recursive walk
        
    

def main():
    path = os.getcwd()
    video_folders = [ f.path for f in os.scandir(path) if f.is_dir() ]
    
    for f in video_folders:
        process_one_folder(f)


if __name__ == "__main__":
    main()

