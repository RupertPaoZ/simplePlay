set pattern_root="Z:/shared_storage/yx.zeng/230929/pattern/128slice"
set save_root="D:/CVPR2024/231009/patterns/128slice"
set pattern_num=128
set frame_num=100

python gen_video.py --pattern_root %pattern_root% --save_root %save_root% --pattern_num %pattern_num% --frame_num %frame_num%