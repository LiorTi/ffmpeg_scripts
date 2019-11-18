import sys
import os
import glob
from send2trash import send2trash # Use: pip install Send2Trash

video_filename_tag = "<in_video-filename>"
video_out_filename_tag = "<out_video-filename>"
resize_width_tag = "<resize_narrow_limit>"
re_compress_ffmpeg_command = \
    f"start /LOW /MIN /WAIT ffmpeg -i {video_filename_tag} -vf \"scale=\'min({resize_width_tag},iw)\':\'min({resize_width_tag},ih)\':force_original_aspect_ratio=decrease\" -sws_flags bilinear -qscale:v 2 {video_out_filename_tag}"


if __name__ == "__main__":

    app_file_name = os.path.basename(sys.argv[0])
    re_encoded_postfix = "_resized"
    print(f"\n\n{app_file_name} version 1.0.2")

    if len(sys.argv) < 3:
        print(f"Use Python {app_file_name} [input mask] [resize max width/height] [-d]")
        print("")
        print("[input mask] - Either a filename or a mask (i.e. *.jpg)")
        print("[resize max width/height] - the smallest width/height for the resized image (i.e. 3000 for maximum width/height of 3000 pixels)")
        print("-d - delete file after compress")
        print("")
        print(f"Note: the app will ignore files with {re_encoded_postfix} string in them.")
        exit(-1)

    delete_source = False
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "-d":
            delete_source = True
            print("enabled option: Delete source files after reencoding...")

    file_list = glob.glob(f"{sys.argv[1]}")
    resize_limit = int(sys.argv[2])
    
    re_compress_ffmpeg_command = re_compress_ffmpeg_command.replace(resize_width_tag, str(resize_limit))

    converted_files_count = 0
    total_space_saved = 0
    for filename in file_list:

        if filename.find(re_encoded_postfix) == -1:
            print(f"Processing: {filename}...  ", end='', flush=True)

            compressed_file_name = filename.replace(".", f"{re_encoded_postfix}.")

            temp_command = re_compress_ffmpeg_command
            temp_command = temp_command.replace(video_filename_tag, filename)
            temp_command = temp_command.replace(video_out_filename_tag, compressed_file_name)
            # print(temp_command)
            os.system(temp_command)
            converted_files_count += 1

            pre_compress_size = int(os.path.getsize(filename) / (1000))
            post_compress_size = int(os.path.getsize(compressed_file_name) / (1000))
            compress_size_diff = pre_compress_size-post_compress_size
            total_space_saved += compress_size_diff
            print(f"completed. {pre_compress_size}KB --> {post_compress_size}KB (saved {compress_size_diff}KB / {int(compress_size_diff * 100 / pre_compress_size)}%)")

            if delete_source:
                print(f"Moving source video to recycle bin: {filename}")
                send2trash(filename)

        else:
            print(f"Skipping an already processed file {filename}")

    print(f"Done. Converted {converted_files_count} files. Saved {total_space_saved}")