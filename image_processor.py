import cv2
import random

class ImageProcessor:
    def __init__(self):
        self.original_image = None
        self.modified_image = None
        self.altered_regions = []       

    def load_image(self, file_path):
        self.original_image = cv2.imread(file_path)
        if self.original_image is None:
            print("Error: Could not load image")
            return None
            
        self.modified_image = self.original_image.copy()
        self.altered_regions = []
        return self.original_image

    def generate_boxes(self, image_height, image_width, region_size=60, num_regions=5):
        selected_regions = []

        while len(selected_regions) < num_regions:
            region_x = random.randint(0, image_width - region_size)
            region_y = random.randint(0, image_height - region_size)
            candidate_region = (region_x, region_y, region_size, region_size)

            has_overlap = False
            for existing_x, existing_y, existing_w, existing_h in selected_regions:
                # basic square overlap check
                regions_overlap = (region_x < existing_x + existing_w and region_x + region_size > existing_x and
                                   region_y < existing_y + existing_h and region_y + region_size > existing_y)
                if regions_overlap:
                    has_overlap = True
                    break

            if not has_overlap:
                selected_regions.append(candidate_region)

        return selected_regions

    def apply_changes(self, canvas, region_x, region_y, region_w, region_h, alteration_type):
        region_pixels = canvas[region_y:region_y + region_h, region_x:region_x + region_w]

        if alteration_type == 1:
            blurred_region = cv2.GaussianBlur(region_pixels, (21, 21), 0)
            canvas[region_y:region_y + region_h, region_x:region_x + region_w] = blurred_region

        elif alteration_type == 2:
            inverted_region = cv2.bitwise_not(region_pixels)
            canvas[region_y:region_y + region_h, region_x:region_x + region_w] = inverted_region

        elif alteration_type == 3:
            circle_center_x = region_x + region_w // 2
            circle_center_y = region_y + region_h // 2
            circle_radius = min(region_w, region_h) // 4
            cv2.circle(canvas, (circle_center_x, circle_center_y), circle_radius, (0, 0, 255), -1)

        elif alteration_type == 4:
            inner_rect_x1 = region_x + region_w // 4
            inner_rect_y1 = region_y + region_h // 4
            inner_rect_x2 = region_x + (3 * region_w) // 4
            inner_rect_y2 = region_y + (3 * region_h) // 4
            cv2.rectangle(canvas, (inner_rect_x1, inner_rect_y1), (inner_rect_x2, inner_rect_y2), (255, 0, 0), -1)

        elif alteration_type == 5:
            channel_swapped = region_pixels.copy()
            channel_swapped[:, :, 0] = region_pixels[:, :, 2]  
            channel_swapped[:, :, 2] = region_pixels[:, :, 0]  
            canvas[region_y:region_y + region_h, region_x:region_x + region_w] = channel_swapped

        return canvas

    def alter_image(self, region_size=60):
        if self.original_image is None:
            print("Error: No image loaded")
            return None

        image_height, image_width = self.original_image.shape[:2]
        self.modified_image = self.original_image.copy()
        self.altered_regions = self.generate_boxes(image_height, image_width, region_size)

        for region_index in range(len(self.altered_regions)):
            region = self.altered_regions[region_index]
            region_x = region[0]
            region_y = region[1]
            region_w = region[2]
            region_h = region[3]
            
            alteration_type = random.randint(1, 5)
            self.modified_image = self.apply_changes(
                self.modified_image, region_x, region_y, region_w, region_h, alteration_type
            )

        return self.modified_image

    def get_altered_regions(self):
        return self.altered_regions

    def draw_circle_on_found(self, canvas, region_x, region_y, region_w, region_h):
        region_center_x = region_x + region_w // 2
        region_center_y = region_y + region_h // 2
        highlight_radius = 40
        cv2.circle(canvas, (region_center_x, region_center_y), highlight_radius, (0, 255, 0), 3)
        return canvas