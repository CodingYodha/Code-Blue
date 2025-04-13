from ultralytics import YOLO
import cv2
import numpy as np
import os
import argparse
import time

def parse_arguments():
    parser = argparse.ArgumentParser(description='Ship detection using YOLOv8')
    parser.add_argument('--model', type=str, default=r"E:\Projects\Code-Blue\ship_detector_model.pt", 
                        help='Path to the trained YOLOv8 model')
    parser.add_argument('--img', type=str, required=True, 
                        help='Path to input image or directory with images')
    parser.add_argument('--conf', type=float, default=0.25, 
                        help='Confidence threshold for detections')
    parser.add_argument('--output', type=str, default='output', 
                        help='Directory to save output images')
    return parser.parse_args()

def process_image(model, image_path, conf_threshold, output_dir):
    """Process a single image and return both image and text results"""
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        return None, f"Error: Could not load image {image_path}"
    
    # Get file name without extension
    file_name = os.path.splitext(os.path.basename(image_path))[0]
    
    # Run inference
    start_time = time.time()
    results = model.predict(img, conf=conf_threshold)
    inference_time = time.time() - start_time
    
    # Get first result
    result = results[0]
    
    # Create text output with detection information
    text_output = f"Results for {image_path}:\n"
    text_output += f"Inference time: {inference_time:.4f} seconds\n"
    
    # Process detections
    boxes = result.boxes
    detection_count = len(boxes)
    text_output += f"Detected {detection_count} ships\n\n"
    
    # Create a copy of the image to draw on
    output_img = img.copy()
    
    # Draw bounding boxes and labels
    for i, box in enumerate(boxes):
        # Get box coordinates
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        
        # Get confidence
        conf = float(box.conf[0])
        
        # Draw bounding box
        cv2.rectangle(output_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Add label
        label = f"Ship: {conf:.2f}"
        cv2.putText(output_img, label, (x1, y1 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Add to text output
        text_output += f"Ship #{i+1}: Confidence={conf:.4f}, Coordinates=[{x1}, {y1}, {x2}, {y2}]\n"
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save output image
    output_path = os.path.join(output_dir, f"{file_name}_detected.jpg")
    cv2.imwrite(output_path, output_img)
    text_output += f"\nOutput image saved to: {output_path}\n"
    
    return output_img, text_output

def main():
    args = parse_arguments()
    
    # Load model
    print(f"Loading model from {args.model}...")
    model = YOLO(args.model)
    print("Model loaded successfully")
    
    # Check if input is a directory or a single image
    if os.path.isdir(args.img):
        # Process all images in directory
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff']
        image_paths = [os.path.join(args.img, f) for f in os.listdir(args.img) 
                      if os.path.splitext(f.lower())[1] in image_extensions]
        
        if not image_paths:
            print(f"No images found in directory {args.img}")
            return
        
        print(f"Found {len(image_paths)} images to process")
        
        # Create text file for all results
        txt_output_path = os.path.join(args.output, "detection_results.txt")
        with open(txt_output_path, 'w') as txt_file:
            txt_file.write(f"Ship Detection Results\n")
            txt_file.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            txt_file.write(f"Model: {args.model}\n")
            txt_file.write(f"Confidence threshold: {args.conf}\n\n")
            
            # Process each image
            for image_path in image_paths:
                print(f"Processing {image_path}...")
                _, text_output = process_image(model, image_path, args.conf, args.output)
                txt_file.write(f"{text_output}\n{'='*50}\n\n")
                
        print(f"All results saved to {txt_output_path}")
        
    else:
        # Process single image
        print(f"Processing image {args.img}...")
        output_img, text_output = process_image(model, args.img, args.conf, args.output)
        
        if output_img is None:
            print(text_output)  # Error message
            return
        
        # Save text output
        txt_output_path = os.path.join(args.output, 
                         f"{os.path.splitext(os.path.basename(args.img))[0]}_results.txt")
        with open(txt_output_path, 'w') as txt_file:
            txt_file.write(text_output)
        
        print(f"Results saved to {txt_output_path}")
        
        # Display result (uncomment if running in an environment with GUI)
        # cv2.imshow("Ship Detection Result", output_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

if __name__ == "__main__":
    main()