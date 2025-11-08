#!/usr/bin/env python3
"""
Analyze audio waveforms of "fortune" pronunciation files.
Generates waveform visualizations and statistical profiles.
"""

import subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path
import json

def extract_audio_data(m4a_file):
    """Extract PCM audio data from m4a file using ffmpeg"""
    try:
        # Convert m4a to raw PCM data
        cmd = [
            'ffmpeg', '-i', str(m4a_file),
            '-f', 's16le',  # 16-bit PCM
            '-acodec', 'pcm_s16le',
            '-ar', '44100',  # Sample rate
            '-ac', '1',  # Mono
            '-'
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            return None, None

        # Convert bytes to numpy array
        audio_data = np.frombuffer(result.stdout, dtype=np.int16)
        sample_rate = 44100

        return audio_data, sample_rate
    except Exception as e:
        print(f"Error processing {m4a_file.name}: {e}")
        return None, None

def analyze_waveform(audio_data, sample_rate):
    """Calculate waveform statistics"""
    if audio_data is None or len(audio_data) == 0:
        return None

    # Normalize to -1 to 1 range
    normalized = audio_data.astype(np.float32) / 32768.0

    stats = {
        'duration': len(audio_data) / sample_rate,
        'max_amplitude': float(np.max(np.abs(normalized))),
        'rms': float(np.sqrt(np.mean(normalized**2))),
        'zero_crossings': int(np.sum(np.diff(np.signbit(normalized)))),
        'dynamic_range': float(np.max(normalized) - np.min(normalized)),
        'samples': len(audio_data)
    }

    return stats, normalized

def plot_waveform(audio_data, sample_rate, title, output_file):
    """Generate waveform visualization"""
    if audio_data is None:
        return

    # Create time axis
    time = np.arange(len(audio_data)) / sample_rate

    # Normalize
    normalized = audio_data.astype(np.float32) / 32768.0

    # Create figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Waveform plot
    ax1.plot(time, normalized, linewidth=0.5, color='#2E86AB')
    ax1.set_xlabel('Time (seconds)', fontsize=10)
    ax1.set_ylabel('Amplitude', fontsize=10)
    ax1.set_title(f'{title}\nWaveform', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-1, 1)

    # Envelope plot
    # Calculate envelope using absolute value and smoothing
    envelope = np.abs(normalized)
    window_size = sample_rate // 100  # 10ms window
    if window_size > 0:
        envelope = np.convolve(envelope, np.ones(window_size)/window_size, mode='same')

    ax2.fill_between(time, envelope, alpha=0.6, color='#A23B72')
    ax2.plot(time, envelope, linewidth=1, color='#F18F01')
    ax2.set_xlabel('Time (seconds)', fontsize=10)
    ax2.set_ylabel('Amplitude Envelope', fontsize=10)
    ax2.set_title('Amplitude Envelope (Energy)', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 1)

    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"  Saved: {output_file.name}")

def main():
    # Directory containing the fortune audio files
    audio_dir = Path.home() / "Music/shakespeare-william/extracts/fortune"
    output_dir = Path.home() / "utono/mccs-fork-manager/my-claude-code-setup/fortune_analysis"

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    print(f"Analyzing audio files in: {audio_dir}\n")

    # Get all m4a files
    audio_files = sorted(audio_dir.glob("*.m4a"))

    if not audio_files:
        print("No m4a files found!")
        return

    all_stats = {}

    for i, audio_file in enumerate(audio_files, 1):
        print(f"[{i}/{len(audio_files)}] Processing: {audio_file.name}")

        # Extract audio data
        audio_data, sample_rate = extract_audio_data(audio_file)

        if audio_data is None:
            print(f"  ⚠ Failed to process")
            continue

        # Analyze waveform
        result = analyze_waveform(audio_data, sample_rate)
        if result:
            stats, normalized = result
            all_stats[audio_file.stem] = stats

            print(f"  Duration: {stats['duration']:.3f}s | RMS: {stats['rms']:.3f} | Peak: {stats['max_amplitude']:.3f}")

            # Generate visualization
            output_file = output_dir / f"{audio_file.stem}_waveform.png"
            plot_waveform(audio_data, sample_rate, audio_file.stem, output_file)

    # Save statistics to JSON
    stats_file = output_dir / "fortune_statistics.json"
    with open(stats_file, 'w') as f:
        json.dump(all_stats, f, indent=2)

    print(f"\n✓ Analysis complete!")
    print(f"  Total files processed: {len(all_stats)}")
    print(f"  Visualizations saved to: {output_dir}")
    print(f"  Statistics saved to: {stats_file}")

    # Print summary statistics
    if all_stats:
        print("\n=== Summary ===")
        durations = [s['duration'] for s in all_stats.values()]
        rms_values = [s['rms'] for s in all_stats.values()]
        print(f"Average duration: {np.mean(durations):.3f}s (±{np.std(durations):.3f}s)")
        print(f"Average RMS amplitude: {np.mean(rms_values):.3f} (±{np.std(rms_values):.3f})")

if __name__ == '__main__':
    main()
