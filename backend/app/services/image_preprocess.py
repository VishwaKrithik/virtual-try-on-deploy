import io
import cv2
import numpy as np
from PIL import Image, ImageFilter


class ImagePreprocessor:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier("app/services/haarcascade_frontalface_default.xml")

    def _resize_person_image(self, person_raw: Image.Image):
        person_raw = person_raw.convert("RGB")
        orig_w, orig_h = person_raw.size

        target_w = 512
        target_h = int(512 * (orig_h / orig_w))
        target_h = max(8, (target_h // 8) * 8)

        person_img = person_raw.resize((target_w, target_h), Image.LANCZOS)
        return person_img, (orig_w, orig_h)

    def _resize_garment_image(self, garment_raw: Image.Image) -> Image.Image:
        return garment_raw.convert("RGB").resize((512, 512), Image.LANCZOS)

    def build_torso_mask(self, person_img: Image.Image) -> Image.Image:
        """
        Detects the face to establish the upper torso baseline, isolates the person's
        silhouette against yellow background, and crops a blurred torso mask.
        """
        person_cv2 = np.array(person_img)
        gray_cv2 = cv2.cvtColor(person_cv2, cv2.COLOR_RGB2GRAY)
        target_h, target_w = gray_cv2.shape

        # 1. Face detection for top boundary offset
        faces = self.face_cascade.detectMultiScale(
            gray_cv2, scaleFactor=1.1, minNeighbors=5
        )

        if len(faces) > 0:
            x, y, w, h = faces[0]
            m_top = y + h + int(h * 0.15)
        else:
            m_top = int(target_h * 0.35)

        # 2. Background thresholding & silhouette isolation
        hsv = cv2.cvtColor(person_cv2, cv2.COLOR_RGB2HSV)
        lower_yellow = np.array([15, 80, 150])
        upper_yellow = np.array([45, 255, 255])

        bg_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        person_silhouette = cv2.bitwise_not(bg_mask)

        kernel = np.ones((5, 5), np.uint8)
        dilated_silhouette = cv2.dilate(
            person_silhouette, kernel, iterations=2)

        # 3. Torso bounding rectangle
        torso_rect = np.zeros_like(gray_cv2)
        cv2.rectangle(
            torso_rect,
            (int(target_w * 0.12), m_top),
            (int(target_w * 0.88), target_h),
            255,
            -1
        )

        # 4. Mask composition & Gaussian edge softening
        final_mask_cv2 = cv2.bitwise_and(torso_rect, dilated_silhouette)
        mask = Image.fromarray(final_mask_cv2).convert("L")
        mask_blurred = mask.filter(ImageFilter.GaussianBlur(radius=6))

        return mask_blurred

    def preprocess(self, person_raw: Image.Image, garment_raw: Image.Image):
        # Unpack image and original size tuple correctly
        person_image, orig_size = self._resize_person_image(
            person_raw=person_raw)
        garment_image = self._resize_garment_image(garment_raw=garment_raw)

        # Generate torso mask from the PIL image
        mask_image = self.build_torso_mask(person_image)

        p_buf, g_buf, m_buf = io.BytesIO(), io.BytesIO(), io.BytesIO()
        person_image.save(p_buf, format="PNG")
        garment_image.save(g_buf, format="PNG")
        mask_image.save(m_buf, format="PNG")

        return {
            "person_bytes": p_buf.getvalue(),
            "garment_bytes": g_buf.getvalue(),
            "mask_bytes": m_buf.getvalue(),
            "orig_size": orig_size
        }


# face_cascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
# )


# def resize_person_image(person_raw: Image.Image):
#     person_raw = person_raw.convert("RGB")
#     orig_w, orig_h = person_raw.size

#     target_w = 512
#     target_h = int(512 * (orig_h / orig_w))
#     target_h = max(8, (target_h // 8) * 8)

#     person_img = person_raw.resize((target_w, target_h), Image.LANCZOS)
#     return person_img, (orig_w, orig_h)


# def resize_garment_image(garment_raw: Image.Image):
#     return garment_raw.convert("RGB").resize((512, 512), Image.LANCZOS)


# def build_torso_mask(person_img: Image.Image):
#     person_cv2 = np.array(person_img)
#     gray_cv2 = cv2.cvtColor(person_cv2, cv2.COLOR_RGB2GRAY)
#     target_h, target_w = gray_cv2.shape

#     faces = face_cascade.detectMultiScale(
#         gray_cv2, scaleFactor=1.1, minNeighbors=5)

#     if len(faces) > 0:
#         x, y, w, h = faces[0]
#         m_top = y + h + int(h * 0.15)
#     else:
#         m_top = int(target_h * 0.35)

#     hsv = cv2.cvtColor(person_cv2, cv2.COLOR_RGB2HSV)
#     lower_yellow = np.array([15, 80, 150])
#     upper_yellow = np.array([45, 255, 255])

#     bg_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
#     person_silhouette = cv2.bitwise_not(bg_mask)

#     kernel = np.ones((5, 5), np.uint8)
#     dilated_silhouette = cv2.dilate(person_silhouette, kernel, iterations=2)

#     torso_rect = np.zeros_like(gray_cv2)
#     cv2.rectangle(
#         torso_rect,
#         (int(target_w * 0.12), m_top),
#         (int(target_w * 0.88), target_h),
#         255,
#         -1
#     )

#     final_mask_cv2 = cv2.bitwise_and(torso_rect, dilated_silhouette)
#     mask = Image.fromarray(final_mask_cv2).convert("L")
#     mask_blurred = mask.filter(ImageFilter.GaussianBlur(radius=6))

#     return mask_blurred


# def remove_garment_background(garment_raw: Image.Image) -> Image.Image:
#     """Removes the background and replaces it with solid white."""
#     # Remove background (returns an RGBA image)
#     bg_removed = remove(garment_raw)

#     # Create a solid white background of the same size
#     white_bg = Image.new("RGB", bg_removed.size, (255, 255, 255))

#     # Paste the isolated garment onto the white background using the alpha channel as a mask
#     white_bg.paste(bg_removed, mask=bg_removed.split()[3])

#     return white_bg


# def build_upper_garment_mask(
#     person_img: Image.Image,
#     protect_lower_body: bool = True,
#     include_arms: bool = False,
# ):
#     """
#     Builds a much stricter upper-body mask so the model edits only the shirt region.
#     This helps prevent:
#     - pants recoloring/generation
#     - unnecessary lower-body edits
#     - sleeve hallucinations from overly large masks
#     """

#     person_cv2 = np.array(person_img)
#     gray_cv2 = cv2.cvtColor(person_cv2, cv2.COLOR_RGB2GRAY)
#     target_h, target_w = gray_cv2.shape

#     faces = face_cascade.detectMultiScale(gray_cv2, scaleFactor=1.1, minNeighbors=5)

#     if len(faces) > 0:
#         x, y, w, h = faces[0]

#         print(faces[0])

#         shoulder_top = y + h + int(h * 0.10)
#         chest_bottom = y + h + int(h * 2.2)
#         torso_center_x = x + w // 2

#         mask_left = max(0, torso_center_x - int(target_w * 0.22))
#         mask_right = min(target_w, torso_center_x + int(target_w * 0.22))
#     else:
#         shoulder_top = int(target_h * 0.22)
#         chest_bottom = int(target_h * 0.58)
#         mask_left = int(target_w * 0.28)
#         mask_right = int(target_w * 0.72)

#     if protect_lower_body:
#         chest_bottom = min(chest_bottom, int(target_h * 0.60))
#     else:
#         chest_bottom = min(chest_bottom, int(target_h * 0.72))

#     base_mask = np.zeros_like(gray_cv2)

#     cv2.rectangle(
#         base_mask,
#         (mask_left, shoulder_top),
#         (mask_right, chest_bottom),
#         255,
#         -1
#     )

#     if include_arms:
#         arm_extension = int(target_w * 0.08)
#         arm_top = shoulder_top + int((chest_bottom - shoulder_top) * 0.08)
#         arm_bottom = shoulder_top + int((chest_bottom - shoulder_top) * 0.55)

#         cv2.rectangle(
#             base_mask,
#             (max(0, mask_left - arm_extension), arm_top),
#             (mask_left, arm_bottom),
#             255,
#             -1
#         )
#         cv2.rectangle(
#             base_mask,
#             (mask_right, arm_top),
#             (min(target_w, mask_right + arm_extension), arm_bottom),
#             255,
#             -1
#         )

#     # optional silhouette refinement from your earlier logic
#     hsv = cv2.cvtColor(person_cv2, cv2.COLOR_RGB2HSV)
#     lower_yellow = np.array([15, 80, 150])
#     upper_yellow = np.array([45, 255, 255])

#     bg_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
#     person_silhouette = cv2.bitwise_not(bg_mask)

#     refined_mask = cv2.bitwise_and(base_mask, person_silhouette)

#     kernel = np.ones((3, 3), np.uint8)
#     refined_mask = cv2.dilate(refined_mask, kernel, iterations=1)

#     mask = Image.fromarray(refined_mask).convert("L")
#     mask_blurred = mask.filter(ImageFilter.GaussianBlur(radius=4))

#     return mask_blurred

# def build_depth_map(person_img: Image.Image, depth_estimator):
#     depth_image = depth_estimator(person_img)["depth"]
#     return depth_image.convert("RGB")
