import os

class EstimationEngine:
    @staticmethod
    def estimate_output(metadata, target_format, preset):
        """
        Estimates output size, quality, and savings percentage.
        """
        input_size = metadata.get('size', 0)
        
        # Default multipliers based on preset and format
        multipliers = {
            'high_quality': {'size': 1.1, 'quality': 95, 'label': 'Excellent'},
            'balanced': {'size': 0.7, 'quality': 85, 'label': 'Very Good'},
            'small_size': {'size': 0.35, 'quality': 65, 'label': 'Optimized'}
        }
        
        m = multipliers.get(preset, multipliers['balanced'])
        
        size_multiplier = m['size']
        quality_score = m['quality']
        quality_label = m['label']
        
        # Target format adjustments
        target_format = target_format.lower()
        if target_format in ['gif']:
            size_multiplier *= 3.0
            quality_score -= 20
        elif target_format in ['webp', 'mp4']:
            size_multiplier *= 0.8 # Better compression
            quality_score += 5
        elif target_format in ['png', 'wav', 'flac']:
            size_multiplier = max(size_multiplier, 0.9) # Lossless/Large
            quality_score = 100
            
        est_size = input_size * size_multiplier
        saving_pct = max(0, round((1 - (est_size / input_size)) * 100)) if input_size > 0 else 0
        
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
            "quality_score": quality_score,
            "savings": f"{saving_pct}%",
            "size_numeric": est_size
        }
