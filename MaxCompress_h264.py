import sys
import os
import glob
from send2trash import send2trash # Use: pip install Send2Trash

MB = 1000*1024
video_filename_tag = "<in_video-filename>"
video_out_filename_tag = "<out_video-filename>"
crf_tag = "<crf>"
re_compress_ffmpeg_command = \
    f"start /LOW /MIN /WAIT ffmpeg -i {video_filename_tag} -c:a copy -c:v libx264 -preset veryslow -crf {crf_tag} {video_out_filename_tag}"


if __name__ == "__main__":

    app_file_name = os.path.basename(sys.argv[0])
    re_encoded_postfix = "_reencoded"
    print(f"\n\n{app_file_name} version 1.1.0")

    crf = 23

    if len(sys.argv) < 2:
        print(f"Use Python {app_file_name} [input mask] [-d] [-quality=#]")
        print("")
        print("[input mask] - Either a filename or a mask (i.e. *.mp4)")
        print("-d - delete file after compress")
        print("-quality=# - Define video quality of output, default 23, 0 = loseless, 51 = lowest quality")
        print("")
        print(f"Note: the app will ignore files with {re_encoded_postfix} string in them.")
        exit(-1)

    delete_source = False
    for i in range(1, len(sys.argv)):
        cmd = sys.argv[i].lower()

        if cmd == "-d":
            delete_source = True
            print("enabled option: Delete source files after reencoding...")
        try:
            [a, v] = cmd.split("=")

            if a == "-quality":
                crf = v
        except:
            print()

    file_list = glob.glob(f"{sys.argv[1]}")

    converted_files_count = 0
    for filename in file_list:

        if filename.find(re_encoded_postfix) == -1:
            print(f"Processing: {filename}...  ", end='', flush=True)

            compressed_file_name = filename.replace(".", f"{re_encoded_postfix}.")

            temp_command = re_compress_ffmpeg_command
            temp_command = temp_command.replace(video_filename_tag, filename)
            temp_command = temp_command.replace(video_out_filename_tag, compressed_file_name)
            temp_command = temp_command.replace(crf_tag, str(crf))
            # print(temp_command)
            os.system(temp_command)
            converted_files_count += 1

            pre_compress_size = os.path.getsize(filename)
            post_compress_size = os.path.getsize(compressed_file_name)
            compress_size_diff = pre_compress_size-post_compress_size
            print(f"completed. {pre_compress_size / MB}MB --> {post_compress_size / MB}MB (saved {compress_size_diff / MB}MB / {int(compress_size_diff * 100 / pre_compress_size)}%)")

            if delete_source:
                print(f"Moving source video to recycle bin: {filename}")
                send2trash(filename)

        else:
            print(f"Skipping an already processed file {filename}")

    print(f"Done. Converted {converted_files_count} files.")