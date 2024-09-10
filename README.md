# GFPGAN Video Face Enhancer

This repository uses GFPGAN 1.4 to enhance faces in a video. The process involves extracting frames from the input video, enhancing the frames using GFPGAN, and then creating a new video from the enhanced frames.

## How It Works

1. **Extract Frames**: The script extracts frames from the input video.
2. **Enhance Frames**: The extracted frames are enhanced using GFPGAN 1.4.
3. **Create Enhanced Video**: The enhanced frames are compiled back into a video.

## Usage

### Input Video

Place your input video in the `inputs` directory with the filename `video.mp4`.

```
/workspace/GFPGAN_video/
├── inputs/
│   └── video.mp4
```

### Running the Script

Run the script `video.py` to process the video:

```sh
python video.py
```

### Output

The enhanced video will be saved in the `outputs` directory as `enhanced_video.mp4`.

```
/workspace/GFPGAN_video/
└── outputs/
    └── enhanced_video.mp4
```

## Colab Notebook

You can also run the process in Google Colab using the following link:

[GFPGAN Video Face Enhancer Colab](https://colab.research.google.com/drive/1sOVfHznU2jFtgO-RvfWr2pXTmuF-mzlh?usp=sharing)

## Example Results

### Before Enhancing

![Before Enhancing](example/before.mp4)

### After Enhancing

![After Enhancing](example/after.mp4)