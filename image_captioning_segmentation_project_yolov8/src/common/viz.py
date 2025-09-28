"""Visualization helpers."""        import numpy as np
import cv2

def overlay_mask_on_image(image: np.ndarray, mask: np.ndarray, alpha: float = 0.5) -> np.ndarray:
    """Overlay a binary mask on an RGB image.

    - `image`: HxWx3 uint8 RGB
    - `mask`: HxW uint8 (0 or 255)
    Returns an RGB uint8 image.
    """
    if mask is None:
        return image
    if image.dtype != 'uint8':
        image = (255 * (image / image.max())).astype('uint8')
    overlay = image.copy()
    # create colored mask (red)
    colored = np.zeros_like(image)
    colored[..., 0] = mask  # red channel
    # blend
    cv2.addWeighted(colored, alpha, overlay, 1 - alpha, 0, overlay)
    # Where mask==0 keep original
    mask_bool = mask.astype(bool)
    result = image.copy()
    result[mask_bool] = overlay[mask_bool]
    return result