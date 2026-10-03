"""
Underwater Image Enhancement Module.
Applies CIELAB color space transformation, adaptive CLAHE on the L* channel,
dynamic noise-type-specific OpenCV filtering (Median/Gaussian/Bilateral),
specular glint suppression, and gamma correction.
"""

from typing import Tuple, Dict, Any, Optional
import cv2
import numpy as np


# Pre-allocated kernel cache for fast morphological filtering
_KERNEL_ELLIPSE_5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
_GAMMA_LUT_CACHE: Dict[float, np.ndarray] = {}


class CLAHEEnhancer:
    """Enhancer using CIELAB color space and Contrast Limited Adaptive Histogram Equalization."""

    def __init__(self, clip_limit: float = 2.5, tile_grid_size: Tuple[int, int] = (8, 8)):
        self.clip_limit = clip_limit
        self.tile_grid_size = tile_grid_size
        self._clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)

    def update_params(self, clip_limit: float, tile_grid_size: Tuple[int, int]):
        """Dynamically updates CLAHE parameters per frame or video condition."""
        grid = (int(tile_grid_size[0]), int(tile_grid_size[1]))
        if abs(clip_limit - self.clip_limit) > 0.05 or grid != self.tile_grid_size:
            self.clip_limit = float(clip_limit)
            self.tile_grid_size = grid
            self._clahe = cv2.createCLAHE(clipLimit=float(clip_limit), tileGridSize=grid)

    def apply(self, bgr_frame: np.ndarray, lab_l_boost: float = 1.0) -> np.ndarray:
        """
        Converts BGR to CIELAB, applies CLAHE to the L* (Luminance) channel,
        scales luminance via fast SIMD convertScaleAbs, and converts back to BGR.
        """
        frame_contig = np.ascontiguousarray(bgr_frame)
        lab = cv2.cvtColor(frame_contig, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)

        # Equalize L channel
        l_enhanced = self._clahe.apply(l_channel)

        if abs(lab_l_boost - 1.0) > 0.01:
            l_enhanced = cv2.convertScaleAbs(l_enhanced, alpha=lab_l_boost)

        lab_enhanced = cv2.merge((l_enhanced, a_channel, b_channel))
        return cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)


def apply_noise_adaptive_filtering(image: np.ndarray, noise_type: str = "Gaussian", denoise_h: float = 4.0) -> np.ndarray:
    """
    Dynamically selects OpenCV filtering kernels based on noise_type from sensory_enhancement.csv:
    - 'SaltPepper' or 'Impulse' -> Median Blur (effective for non-linear impulse noise)
    - 'Poisson' -> Gaussian Blur (mitigates Poisson shot noise)
    - 'Gaussian' or 'Speckle' -> Bilateral Filter (preserves sharp shrimp contours & antennae)
    """
    if image is None or image.size == 0:
        return image

    img = np.ascontiguousarray(image)
    n_type = str(noise_type).lower().strip()

    if "salt" in n_type or "pepper" in n_type or "impulse" in n_type:
        ksize = 5 if denoise_h >= 5.0 else 3
        return cv2.medianBlur(img, ksize)

    elif "poisson" in n_type:
        sigma = 1.0 + (denoise_h * 0.2)
        return cv2.GaussianBlur(img, (5, 5), sigmaX=sigma, sigmaY=sigma)

    else:
        d = 7
        sigma_color = float(denoise_h * 8)
        sigma_space = float(denoise_h * 4)
        return cv2.bilateralFilter(img, d=d, sigmaColor=sigma_color, sigmaSpace=sigma_space)


def suppress_light_glint(image: np.ndarray, reflection_mask_sum: float = 2000.0) -> np.ndarray:
    """
    Suppresses specular reflection on water surface by dampening saturated highlights,
    scaled by reflection_mask_sum from light_reflection.csv.
    """
    if image is None or image.size == 0 or reflection_mask_sum < 1000.0:
        return image

    img = np.ascontiguousarray(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    thresh_val = 230 if reflection_mask_sum > 3000 else 240
    _, highlight_mask = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)

    if cv2.countNonZero(highlight_mask) > 0:
        highlight_mask = cv2.dilate(highlight_mask, _KERNEL_ELLIPSE_5, iterations=1)
        blurred_fill = cv2.GaussianBlur(img, (15, 15), 0)
        dampened = cv2.addWeighted(img, 0.40, blurred_fill, 0.60, 0)
        mask_3ch = cv2.merge([highlight_mask, highlight_mask, highlight_mask])
        return np.where(mask_3ch == 255, dampened, img).astype(np.uint8)

    return img


def apply_gamma_correction(image: np.ndarray, gamma: float = 1.0) -> np.ndarray:
    """Applies power-law gamma transformation using cached 256-value LUT."""
    if image is None or image.size == 0:
        return image

    gamma_rounded = round(float(gamma), 3)
    if abs(gamma_rounded - 1.0) < 1e-3:
        return image

    if gamma_rounded not in _GAMMA_LUT_CACHE:
        inv_gamma = 1.0 / max(gamma_rounded, 1e-4)
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype("uint8")
        _GAMMA_LUT_CACHE[gamma_rounded] = table

    return cv2.LUT(np.ascontiguousarray(image), _GAMMA_LUT_CACHE[gamma_rounded])


def enhance_underwater_frame(
    frame: np.ndarray,
    params: Optional[Dict[str, Any]] = None,
    enhancer_cache: Optional[CLAHEEnhancer] = None,
) -> np.ndarray:
    """
    Full dynamic underwater enhancement pipeline connecting all 5 CSV data parameters:
    1. Specular Glint Suppression (light_reflection.csv: reflection_mask_sum)
    2. CIELAB adaptive histogram equalization (light_reflection.csv: clahe_clip_limit)
    3. Dynamic Noise-Type Adaptive Filtering (sensory_enhancement.csv: noise_type)
    4. Gamma correction
    """
    if frame is None or frame.size == 0:
        return frame

    processed = np.ascontiguousarray(frame)
    if len(processed.shape) == 2:
        processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
    elif processed.shape[2] == 4:
        processed = cv2.cvtColor(processed, cv2.COLOR_BGRA2BGR)

    if params is None:
        params = {}

    clip_limit = float(params.get("clahe_clip_limit", 2.5))
    raw_tile_grid = params.get("clahe_tile_grid_size", (8, 8))
    tile_grid = (int(raw_tile_grid[0]), int(raw_tile_grid[1]))
    noise_type = params.get("noise_type", "Gaussian")
    denoise_h = float(params.get("denoise_h", 4.0))
    reflection_mask_sum = float(params.get("reflection_mask_sum", 2000.0))
    lab_l_boost = float(params.get("lab_l_boost", 1.05))
    gamma = float(params.get("gamma_correction", 0.98))

    # 1. Specular glint suppression (dampens blinding surface reflection glare)
    processed = suppress_light_glint(processed, reflection_mask_sum=reflection_mask_sum)

    # 2. CIELAB + CLAHE on L* channel (restores contrast through turbid water)
    if enhancer_cache is not None:
        enhancer_cache.update_params(clip_limit, tile_grid)
        processed = enhancer_cache.apply(processed, lab_l_boost=lab_l_boost)
    else:
        enhancer = CLAHEEnhancer(clip_limit=clip_limit, tile_grid_size=tile_grid)
        processed = enhancer.apply(processed, lab_l_boost=lab_l_boost)

    # 3. Dynamic Noise-Type Adaptive Filtering (smooths background noise amplified by CLAHE, preserving boundaries)
    processed = apply_noise_adaptive_filtering(processed, noise_type=noise_type, denoise_h=denoise_h)

    # 4. Gamma correction
    if abs(gamma - 1.0) > 1e-3:
        processed = apply_gamma_correction(processed, gamma=gamma)

    return processed
