import cv2
import os
import imutils

# Draw a colored mask on the input image based on specified borders.
def draw_color_mask(img, borders, color=(0, 0, 0)):
    h = img.shape[0]
    w = img.shape[1]

    x_min = int(borders[0] * w / 100)
    x_max = w - int(borders[2] * w / 100)
    y_min = int(borders[1] * h / 100)
    y_max = h - int(borders[3] * h / 100)

    img = cv2.rectangle(img, (0, 0), (x_min, h), color, -1)
    img = cv2.rectangle(img, (0, 0), (w, y_min), color, -1)
    img = cv2.rectangle(img, (x_max, 0), (w, h), color, -1)
    img = cv2.rectangle(img, (0, y_max), (w, h), color, -1)

    return img


# Preprocess the input image for change detection.
def preprocess_image_change_detection(img, gaussian_blur_radius_list=None, black_mask=(5, 10, 5, 0)):
    gray = img.copy()
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    if gaussian_blur_radius_list is not None:
        for radius in gaussian_blur_radius_list:
            gray = cv2.GaussianBlur(gray, (radius, radius), 0)

    gray = draw_color_mask(gray, black_mask)

    return gray


# Compare two frames for change detection.
def compare_frames_change_detection(prev_frame, next_frame, min_contour_area):
    frame_delta = cv2.absdiff(prev_frame, next_frame)
    thresh = cv2.threshold(frame_delta, 45, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    score = 0
    res_cnts = []
    for c in cnts:
        if cv2.contourArea(c) < min_contour_area:
            continue

        res_cnts.append(c)
        score += cv2.contourArea(c)

    return score, res_cnts, thresh


# solution code begins from here

# read image 2 images from the provided image path, resize them to common size, apply gaussian blur, black mask on the edges and calculate difference score
def process_images(image_path1, image_path2, target_resolution, gaussian_blur_radius_list, black_mask, min_contour_area):
    try:
        # Load images
        image1 = cv2.imread(image_path1)
        image2 = cv2.imread(image_path2)

        # Check if images are successfully loaded
        if image1 is None or image2 is None:
            print(f"Error loading images: {image_path1}, {image_path2}")
            return None, None

        # Resize images to the common resolution
        resized_image1 = cv2.resize(image1, target_resolution)
        resized_image2 = cv2.resize(image2, target_resolution)

        # Preprocess images
        processed_image1 = preprocess_image_change_detection(resized_image1, gaussian_blur_radius_list, black_mask)
        processed_image2 = preprocess_image_change_detection(resized_image2, gaussian_blur_radius_list, black_mask)

        # Compare frames
        score, contours, _ = compare_frames_change_detection(processed_image1, processed_image2, min_contour_area)

        return score, len(contours)

    except Exception as e:
        print(f"Error processing images: {str(e)}")
        return None, None

# Set parameters
target_resolution = (800, 600) # common resolution to prevent runtime error with cv2 
gaussian_blur_radius_list = [9] # appropriate chosen blur radius value
min_contour_area = 25 # chosen contour area value for considering significant change
black_mask = (5, 10, 5, 0) # provided by kopernikus

# Ask the user to enter the target folder path
target_folder = input("Enter the target folder path containing PNG images: ")

# Get a list of PNG files in the target folder
png_files = [file for file in os.listdir(target_folder) if file.lower().endswith('.png')]

# Iterate over pairs of images for comparison
for i in range(len(png_files) - 1):
    image_path1 = os.path.join(target_folder, png_files[i])
    image_path2 = os.path.join(target_folder, png_files[i + 1])

    # Process images and get similarity scores
    similarity_score, num_contours = process_images(image_path1, image_path2, target_resolution, gaussian_blur_radius_list, black_mask, min_contour_area)

    # Delete image2 if the change score is less than 300
    if similarity_score is not None and similarity_score < 300:
        try:
            os.remove(image_path1)
            print(f"Deleted {image_path1} due to low change score.")
        except Exception as e:
            print(f"Error deleting {image_path1}: {str(e)}")

    # Display results if the processing is successful
    if similarity_score is not None and num_contours is not None:
        print(f"Comparison between {png_files[i]} and {png_files[i + 1]}:")
        print(f"Change Score: {similarity_score}")
        print(f"Number of Contours: {num_contours}")
        print("\n")

png_files_post = [file for file in os.listdir(target_folder) if file.lower().endswith('.png')]
print(f'Original number of png files in the folder {target_folder}: {len(png_files)}')
print(f'Final Number of png files in the folder {target_folder}: {len(png_files_post)}')