#!/usr/bin/env python3
"""
Extract all occurrences of the word "fortune" from an audiobook.
Uses Whisper for speech recognition with word-level timestamps.
"""

import whisper
import subprocess
import json
from pathlib import Path
from datetime import datetime
import re

def transcribe_audio(audio_file, model_name="base"):
    """
    Transcribe audio with word-level timestamps using Whisper.
    Returns word segments with start/end times.
    """
    print(f"Loading Whisper model '{model_name}'...")
    model = whisper.load_model(model_name)

    print(f"Transcribing {audio_file.name} (this may take a while)...")
    result = model.transcribe(
        str(audio_file),
        word_timestamps=True,
        verbose=False
    )

    return result

def find_word_occurrences(transcription, target_word):
    """
    Find all occurrences of a target word in the transcription.
    Returns list of word dictionaries with timing info.
    """
    occurrences = []
    target_lower = target_word.lower()

    for segment in transcription.get('segments', []):
        for word_info in segment.get('words', []):
            word_text = word_info.get('word', '').strip().lower()
            # Remove punctuation for comparison
            word_clean = re.sub(r'[^\w\s]', '', word_text)

            if word_clean == target_lower:
                occurrences.append({
                    'word': word_info.get('word'),
                    'start': word_info.get('start'),
                    'end': word_info.get('end'),
                    'segment_text': segment.get('text', '')
                })

    return occurrences

def extract_audio_segment(input_file, output_file, start_time, duration):
    """
    Extract a segment from audio file using ffmpeg.
    """
    cmd = [
        'ffmpeg', '-y',
        '-i', str(input_file),
        '-ss', str(start_time),
        '-t', str(duration),
        '-c', 'copy',
        '-avoid_negative_ts', 'make_zero',
        str(output_file)
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def format_timestamp(seconds):
    """Convert seconds to HH_MM_SS format for filenames."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}_{minutes:02d}_{secs:02d}"

def main():
    # Configuration
    audiobook_path = Path("/home/mlj/Music/shakespeare-william/aax-Arkangel/TroilusandCressidaArkangelShakespeare_ep7.m4b")
    output_dir = Path("/home/mlj/Music/shakespeare-william/extracts/fortune/auto_extracted")
    target_word = "fortune"
    context_seconds = 6  # seconds before and after the word
    total_duration = context_seconds * 2

    # Whisper model options: tiny, base, small, medium, large
    # base is a good balance of speed and accuracy
    model_name = "base"

    print("=" * 70)
    print("FORTUNE WORD EXTRACTOR")
    print("=" * 70)
    print(f"Audiobook: {audiobook_path.name}")
    print(f"Target word: '{target_word}'")
    print(f"Context: {context_seconds}s before + {context_seconds}s after = {total_duration}s clips")
    print(f"Whisper model: {model_name}")
    print("=" * 70)
    print()

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Transcribe audio
    transcription = transcribe_audio(audiobook_path, model_name)

    # Save full transcription for reference
    transcript_file = output_dir / "full_transcription.json"
    with open(transcript_file, 'w') as f:
        json.dump(transcription, f, indent=2)
    print(f"✓ Full transcription saved to: {transcript_file}")

    # Find all occurrences of target word
    print(f"\nSearching for '{target_word}' in transcription...")
    occurrences = find_word_occurrences(transcription, target_word)

    if not occurrences:
        print(f"No occurrences of '{target_word}' found!")
        return

    print(f"✓ Found {len(occurrences)} occurrence(s) of '{target_word}'")
    print()

    # Extract audio segments
    success_count = 0
    occurrences_info = []

    for i, occurrence in enumerate(occurrences, 1):
        word_start = occurrence['start']
        word_end = occurrence['end']
        word_center = (word_start + word_end) / 2

        # Calculate extraction boundaries
        extract_start = max(0, word_center - context_seconds)

        # Create output filename with timestamp
        timestamp_str = format_timestamp(word_start)
        output_file = output_dir / f"fortune_{i:02d}_at_{timestamp_str}.m4a"

        print(f"[{i}/{len(occurrences)}] Extracting occurrence at {word_start:.2f}s")
        print(f"  Context: '{occurrence['segment_text'].strip()}'")
        print(f"  Time range: {extract_start:.2f}s - {extract_start + total_duration:.2f}s")

        # Extract segment
        success = extract_audio_segment(
            audiobook_path,
            output_file,
            extract_start,
            total_duration
        )

        if success:
            print(f"  ✓ Saved: {output_file.name}")
            success_count += 1

            occurrences_info.append({
                'index': i,
                'word_time': word_start,
                'extract_start': extract_start,
                'extract_end': extract_start + total_duration,
                'context': occurrence['segment_text'].strip(),
                'filename': output_file.name
            })
        else:
            print(f"  ✗ Failed to extract")

        print()

    # Save occurrence info
    info_file = output_dir / "fortune_occurrences.json"
    with open(info_file, 'w') as f:
        json.dump(occurrences_info, f, indent=2)

    print("=" * 70)
    print("EXTRACTION COMPLETE")
    print("=" * 70)
    print(f"Total occurrences found: {len(occurrences)}")
    print(f"Successfully extracted: {success_count}")
    print(f"Output directory: {output_dir}")
    print(f"Occurrence details: {info_file}")
    print("=" * 70)

if __name__ == '__main__':
    main()
