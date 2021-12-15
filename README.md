# [CS341] Experimental Grib 2 Repository

This repo contains modified code from ECCODES library. The modified codefile is grib_openjpeg_encoding.c. This repository is not intended for consumer use and is only for developmental purposes. The goals of this project are the following:

* [**Analysis**] Understand the architecture of Grib2 and how the methods are connected
* [**Implementation**] Reconstruct Grib2 JP2000 encoder and decoder methods so that
  * The encoder produces encoded image files instead of the normal behavior where the encoder saves the encoded image within the Grib file
  * The decoder uses external encoded image files instead of the normal behavior where the decoder accesses the memory address of a buffer
* [**Video Codec Encoding**] Encode the results of the modified Encoder image files using FFMPEG libx264 video codec
* [**Video Decoding**] Decode the video frames back into individual uncompressed images
* [**Analysis**] Compare between the original uncompressed images and the images that were decoded from the video using PSNR as a metric
* [**Analysis**] Compute the MSE between the original floating point values and the encoded values

In the report, we discuss the results of these goals in great details. 

## Installation and Use

In order to install and run the code, you should follow the installation instruction of the original eccodes library and install any needed dependencies. Once you clone eccodes, you should replace the grib_openjpeg_encoding.c from this repository with the original eccodes file. Installation of Eccodes will require using CMake and Make. Now after installing and creating the executable binaries, you should be concerned about two files:

* grib_accessor_class_data_jpeg2000.c
* grib_openjpeg_encoding.c

The accessor class is used\triggered whenever the grib library detects what kind of packing and compression have been used. The accessor class controls the rate of execution of grib_openjpeg_encoding and all its methods. Now, grib_openjpeg_encoding might seem messy. You will find two encode and decode methods respectively

* grib_openjpeg_encode_old
* grib_openjpeg_decode_old
* grib_openjpeg_encode
* grib_openjpeg_decode

Grib2 only uses grib_openjpeg_encode and grib_openjpeg_decode. In order to use the old encoder & decoder, you have to rename them back to grib_openjpeg_encode and decode respectively (while renaming the others to something else). Now why is it like this and what is the difference between them? The old encoder\decoder are memory-based methods. We use them in the following scenarios:

* When you need to save the data within the grib file, you may use grib_openjpeg_decode_old
* When you need to compress the data and save it within the file, you may use grib_openjpeg_encode_old
* When you need to write out the compresseed images and read from them, you may use the non-old decode and encode.

There are also cases where you might need to use the old encode with the new decoder. For instance, in order to read the images that resulted from decoding a video and encode them within the gribfile in order to manipulate the data further, you will need to use the new decoder with the old encoder. You might also use the new encoder in order to write out the JP2000 images that can be used later in video compression.

## Execution Flow

In this section, I will describe the execution flow required in order to create a compresed video of grib messages and evaluate them. Note: Whenever I say "we use the old encoder" or the ".. use the new encoder".. it means you have to do the renamings and rebuild the source.

1. Given a grib file with many timesteps and one attribute, we run the new encode method to generate a directory of Encoded Images using the command grib_set
2. We run the following command: ffmpeg ... in order to encode the Encoded Images into a Video with codec libx264 and crf 18 (Lossy Compression)
3. We decode the video back into individual images using ffmpeg
4. We may use the python script image_eval.py in the scripts directory to compute the PSNR between the images in Step 1 and Step 3.
5. We use the new decoder with the old encoder in order to create a new grib (let's call it Temp_VidCodecs_Imgs.grb2) file using the command grib_set
6. We use grib_dump -j Temp_VidCodecs_Imgs.grb2 >> dump.json in order to generate all the floating point numbers of Temperature
7. Assuming we have a json dump of the original floating numbers, we compare between these two json files by computing MSE_calc in scripts directory

This concludes a basic execution flow. Please note that some directories are hardcoded, so you will need to have understand and look at the methods implemented in grib_openjpeg_encode.c. The figure below provides an overview of how the system works.

![image](https://user-images.githubusercontent.com/31670621/146174734-692a44fc-70c5-42ac-9bbf-372509ba177d.png)


## Resources

- https://confluence.ecmwf.int/display/ECC/
- https://github.com/AZed/cdo
- https://github.com/ecmwf/eccodes-python
- https://link.springer.com/content/pdf/10.1007%2F978-3-642-38750-0.pdf (On compression)
- https://code.mpimet.mpg.de/attachments/download/13557/CDO_Seminar_20161206.pdf
- https://code.mpimet.mpg.de/projects/cdo/wiki/Tutorial
- https://code.mpimet.mpg.de/attachments/download/13557/CDO_Seminar_20161206.pdf
- https://www.unidata.ucar.edu/software/netcdf/workshops/2008/utilities/Cdo.html
- [http://xarray.pydata.org/en/stable/index.html#:~:text=xarray%20%28formerly%20xray%29%20is%20an%20open%20source%20project,with%20labelled%20multi-dimensional%20arrays%20simple%2C%20efficient%2C%20and%20fun%21](http://xarray.pydata.org/en/stable/index.html#:~:text=xarray (formerly xray) is an open source project,with labelled multi-dimensional arrays simple%2C efficient%2C and fun!)

## Ask me and Contact

For any questions\queries, please reach out to me at asaadge@gmail.com. Thank you for your time.

Sincerely,
Asaad Alghamdi
