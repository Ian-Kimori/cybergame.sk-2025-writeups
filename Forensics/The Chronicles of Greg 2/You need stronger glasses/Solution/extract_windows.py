import os

import cv2

# If true, shows a preview of the template to search for in other frames
SHOW_BINDING_BOX = True

# If true, also exports 'full_windows', not just 'windows' with mosaics-only
EXPORT_FULL_WINDOWS = True

# Bounding box coordinates - template to search for in other frames
x, y, bb_w, bb_h, win_w, win_h = 1685, 645, 600, 1250, 1880, 1280

# Coordinates of the censored mosaic in the first frame - used to cut just that part out
mos_x, mos_y, mos_w, mos_h = 2265, 970, 950, 456

# Create output directory
os.makedirs('windows', exist_ok=True)
if EXPORT_FULL_WINDOWS:
    os.makedirs('full_windows', exist_ok=True)

# Load initial frame
frame = cv2.imread('frames/0001.png')
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Draw bounding box for adjustment
frame_with_box = frame.copy()
cv2.rectangle(frame_with_box, (x, y), (x + bb_w, y + bb_h), (255, 0, 0), 2)

if SHOW_BINDING_BOX:
    # Show bounding box on initial frame
    cv2.imshow('Adjust Bounding Box', frame_with_box)
    cv2.waitKey(0)

template = gray[y:y + bb_h, x:x + bb_w]

# Process other frames via template matching
frame_dir = 'frames'
for fname in sorted(os.listdir(frame_dir)):
    if not fname.endswith('.png'):
        continue
    print(f'Processing {fname}...')
    full_path = os.path.join(frame_dir, fname)
    img = cv2.imread(full_path)
    if img is None:
        continue

    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Match template
    method = cv2.TM_SQDIFF_NORMED
    res = cv2.matchTemplate(gray_frame, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # max_loc is the top‑left corner of a detected window
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
        confidence = 1 - min_val
    else:
        top_left = max_loc
        confidence = max_val

    bottom_right = (top_left[0] + win_w, top_left[1] + win_h)

    # Optional: sanity‑check match quality
    if confidence < 0.95:
        print(f'Low confidence ({confidence:.2f}) for {fname}, skipping.')
        continue
    else:
        print(f'Good confidence ({confidence}) for {fname}, saving.')

    if EXPORT_FULL_WINDOWS:
        crop = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        cv2.imwrite(os.path.join('full_windows', fname), crop)

    mos_top_left = (top_left[0] + (mos_x - x), top_left[1] + (mos_y - y))
    mos_bottom_right = (mos_top_left[0] + mos_w), (mos_top_left[1] + mos_h)
    mos_crop = img[mos_top_left[1]:mos_bottom_right[1], mos_top_left[0]:mos_bottom_right[0]]
    cv2.imwrite(os.path.join('windows', fname), mos_crop)
