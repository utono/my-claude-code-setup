#!/usr/bin/env python3
"""
Transcribe a 10-minute audio segment and find occurrences of "fortune".
"""
import whisper
import json
from pathlib import Path

def transcribe_and_find_fortune(audio_file, start_offset=5400):
    """
    Transcribe audio segment and locate all "fortune" occurrences.

    Args:
        audio_file: Path to audio file to transcribe
        start_offset: The offset in seconds where this segment starts in the full audiobook
    """
    print(f"Loading Whisper model...")
    model = whisper.load_model("base")

    print(f"\nTranscribing: {audio_file}")
    print("This will take 2-3 minutes for a 10-minute segment...\n")

    # Transcribe with word-level timestamps
    result = model.transcribe(
        str(audio_file),
        word_timestamps=True,
        language="en"
    )

    # Find all occurrences of "fortune"
    fortune_occurrences = []

    for segment in result['segments']:
        if 'words' in segment:
            for word in segment['words']:
                word_text = word['word'].strip().lower().strip('.,!?;:')
                if 'fortune' in word_text:
                    # Adjust timestamps to account for segment position in full file
                    actual_start = start_offset + word['start']
                    actual_end = start_offset + word['end']

                    fortune_occurrences.append({
                        'word': word['word'],
                        'segment_start': word['start'],
                        'segment_end': word['end'],
                        'actual_start': actual_start,
                        'actual_end': actual_end,
                        'context': segment['text']
                    })

    return fortune_occurrences, result

def main():
    audio_file = Path("/tmp/troilus_middle_10min.m4a")
    output_dir = Path.home() / "Music/shakespeare-william/extracts/fortune"

    if not audio_file.exists():
        print(f"Error: Audio file not found: {audio_file}")
        return

    # Transcribe and find fortune occurrences
    occurrences, full_transcript = transcribe_and_find_fortune(audio_file)

    # Save results
    results = {
        'segment_info': {
            'source': 'TroilusandCressidaArkangelShakespeare_ep7.m4b',
            'segment_start': 5400,  # 90 minutes
            'segment_duration': 600,  # 10 minutes
            'segment_file': str(audio_file)
        },
        'fortune_occurrences': occurrences,
        'full_transcript': full_transcript['text']
    }

    output_file = output_dir / "segment_transcription_results.json"
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    # Print summary
    print("\n" + "="*70)
    print("TRANSCRIPTION COMPLETE")
    print("="*70)
    print(f"\nSegment: 90:00 - 100:00 (middle of audiobook)")
    print(f"Found {len(occurrences)} occurrence(s) of 'fortune'\n")

    if occurrences:
        for i, occ in enumerate(occurrences, 1):
            minutes = int(occ['actual_start'] // 60)
            seconds = int(occ['actual_start'] % 60)
            print(f"{i}. At {minutes:02d}:{seconds:02d} - '{occ['word']}'")
            print(f"   Context: {occ['context'][:100]}...")
            print()
    else:
        print("No occurrences of 'fortune' found in this 10-minute segment.")
        print("You may need to check other segments of the audiobook.")

    print(f"\nFull results saved to: {output_file}")
    print(f"\nTranscript preview:")
    print("-" * 70)
    print(full_transcript['text'][:500] + "...")

if __name__ == "__main__":
    main()
