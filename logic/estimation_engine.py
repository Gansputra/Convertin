import os

class EstimationEngine:
    @staticmethod
    def estimate_output(metadata, target_format, preset):
        """
        Estimates output size, quality, and processing time.
        """
        input_size = metadata.get('size', 0)
        duration = metadata.get('duration', 0)
        
        # Default multipliers
        size_multiplier = 1.0
        time_multiplier = 1.0
        quality_label = "Good"
        
        if preset == 'high_quality':
            size_multiplier = 1.5
            time_multiplier = 2.0
            quality_label = "Premium / Lossless"
        elif preset == 'balanced':
            size_multiplier = 0.8
            time_multiplier = 1.0
            quality_label = "High / Standard"
        elif preset == 'small_size':
            size_multiplier = 0.4
            time_multiplier = 0.7
            quality_label = "Reduced / Compressed"
            
        # Target format affects size too
        if target_format == 'gif':
            size_multiplier *= 3.0 # GIFs are huge
        elif target_format == 'pdf':
            size_multiplier *= 0.5
            
        est_size = input_size * size_multiplier
        
        # Process time estimation (very rough: 1 second per 10MB as base)
        base_time = (input_size / (1024 * 1024)) * 0.5 # 0.5s per MB
        est_time = base_time * time_multiplier
        
        # Format size for display
        def format_size(size):
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024:
                    return f"{size:.1f} {unit}"
                size /= 1024
            return f"{size:.1f} TB"

        return {
            "estimated_size": format_size(est_size),
            "estimated_quality": quality_label,
            "estimated_time": f"{max(1, round(est_time))} seconds",
            "size_numeric": est_size
        }
