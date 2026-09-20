# Verification

The generated package must satisfy:

- 6 narration WAV sections, all readable and non-empty
- total narration duration between 180 and 480 seconds
- 8 original 1920×1080 visuals
- 3 original 1280×720 thumbnails
- generated assembly map uses actual narration WAV durations
- no external media downloads
- source docs remain text-reviewable
- generation is deterministic except for WAV codec/container metadata produced by eSpeak NG

Generation happens in GitHub Actions and commits the produced assets back to the package branch.

The workflow prints dimensions, audio durations, total duration, asset counts, and SHA-256 hashes for reviewer verification.
