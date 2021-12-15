import argparse
import os
import cv2
import pandas as pd
from skimage.metrics import peak_signal_noise_ratio

parser = argparse.ArgumentParser(description='image_eval')
parser.add_argument('--orig_path',help='path to orig image dataset', default='orig/')
parser.add_argument('--recon_path',help='path to recon image dataset', default='recon/')
parser.add_argument('--image_format',help='format of the image', default='bmp')
opt = parser.parse_args()

num_files = 0
for fn in os.listdir(opt.orig_path):
    num_files += 1
    
offset = 7977
for idx in range(num_files):

    locals()['orig_'+str(idx+offset)+''] = cv2.imread('%s/%d.%s' %(opt.orig_path,idx+offset,opt.image_format))
    print('%s/%d.%s' %(opt.orig_path,idx+offset,opt.image_format))
    locals()['recon_'+str(idx+offset)+''] = cv2.imread('%s/%d.%s' %(opt.recon_path,idx+offset,opt.image_format))

    locals()['psnr_'+str(idx+offset)+''] = peak_signal_noise_ratio(locals()['orig_'+str(idx+offset)+''],locals()['recon_'+str(idx+offset)+''])
    # locals()['ssim_'+str(idx+offset)+''] = compare_ssim(locals()['orig_'+str(idx+offset)+''],locals()['recon_'+str(idx+offset)+''],multichannel=False)


    image_number = (str(idx+offset))
    psnr_number = (locals()['psnr_'+str(idx+offset)+''])
    # ssim_number.append(locals()['ssim_'+str(idx+offset)+''])
    print(psnr_number)
    dit = {'image_number':image_number, 'psnr':psnr_number}
    df = pd.DataFrame(dit, index=["image_number", "psnr"])
    df.to_csv('result.csv', mode='a', index=False,header=False)
