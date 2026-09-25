import os
from PIL import Image

def crop_and_resize(img_path, out_path, target_ratio, target_width):
    if not os.path.exists(img_path):
        return
    
    img = Image.open(img_path)
    w, h = img.size
    current_ratio = w / h
    
    # Calculate crop box
    if current_ratio > target_ratio:
        # Image is wider than needed, crop width
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        right = left + new_w
        top = 0
        bottom = h
    else:
        # Image is taller than needed, crop height
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        bottom = top + new_h
        left = 0
        right = w
        
    cropped = img.crop((left, top, right, bottom))
    
    # Resize to standard width
    target_height = int(target_width / target_ratio)
    resized = cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    # Save
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    resized.save(out_path, quality=90)
    print(f"Saved {out_path}")

def pad_to_ratio(img_path, out_path, target_ratio, target_width):
    if not os.path.exists(img_path):
        return
    img = Image.open(img_path)
    w, h = img.size
    current_ratio = w / h
    
    if current_ratio >= target_ratio:
        # Already wide enough, maybe just resize
        target_height = int(target_width / target_ratio)
        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        padded = img
    else:
        # Need to pad width
        new_w = int(h * target_ratio)
        padded = Image.new("RGB", (new_w, h), (255, 255, 255))
        padded.paste(img, ((new_w - w) // 2, 0))
        target_height = int(target_width / target_ratio)
        padded = padded.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    padded.save(out_path, quality=90)
    print(f"Saved {out_path}")

# Main image for banners
main_img = "images/family/mama-dcery-srdce.jpg"
out_dir = "images/sklik_banners/"

crop_and_resize(main_img, out_dir + "kombinovana_1200x628.jpg", 1.91/1, 1200)
crop_and_resize(main_img, out_dir + "kombinovana_1200x1200.jpg", 1/1, 1200)
crop_and_resize(main_img, out_dir + "kombinovana_1200x900.jpg", 4/3, 1200)

# Logo
logo_img = "logo.jpg"
pad_to_ratio(logo_img, out_dir + "logo_1_1.jpg", 1/1, 512)
pad_to_ratio(logo_img, out_dir + "logo_4_1.jpg", 4/1, 1024)

