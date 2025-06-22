import numpy as np
import time
from PIL import Image

class PCAImageCompressor:
    def __init__(self):
        self.runtime = 0
        self.compression_stats = {}
    
    def compress_image_pca(self, image_array, n_components):
        start_time = time.time()
        
        # Handle different image types
        if len(image_array.shape) == 3:  # Color image (RGB)
            compressed_channels = []
            for channel in range(image_array.shape[2]):
                channel_data = image_array[:, :, channel].astype(np.float64)
                compressed_channel = self._pca_compress_channel(channel_data, n_components)
                compressed_channels.append(compressed_channel)
            compressed_image = np.stack(compressed_channels, axis=2)
        else:  # Grayscale image
            compressed_image = self._pca_compress_channel(image_array.astype(np.float64), n_components)
        
        compressed_image = np.clip(compressed_image, 0, 255).astype(np.uint8)
        end_time = time.time()
        self.runtime = end_time - start_time
        
        self._calculate_stats(image_array, compressed_image, n_components)
        return compressed_image

    def _pca_compress_channel(self, channel_data, n_components):
        mean_data = np.mean(channel_data, axis=0)
        centered_data = channel_data - mean_data
        covariance_matrix = np.dot(centered_data.T, centered_data) / (centered_data.shape[0] - 1)
        eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
        idx = np.argsort(eigenvalues)[::-1]
        eigenvectors_sorted = eigenvectors[:, idx]
        
        n_components = min(n_components, eigenvectors_sorted.shape[1])
        selected_eigenvectors = eigenvectors_sorted[:, :n_components]

        projected_data = np.dot(centered_data, selected_eigenvectors)
        reconstructed_data = np.dot(projected_data, selected_eigenvectors.T) + mean_data
        return reconstructed_data

    def _calculate_stats(self, original, compressed, n_components):
        mse = np.mean((original.astype(np.float64) - compressed.astype(np.float64)) ** 2)
        if mse == 0:
            psnr = float('inf')
        else:
            psnr = 20 * np.log10(255.0 / np.sqrt(mse))
        self.compression_stats = {
            "mse": mse,
            "psnr": psnr,
            "components": n_components,
            "runtime": self.runtime
        }

    def get_stats(self):
        return self.compression_stats
        