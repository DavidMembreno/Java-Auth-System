import cv2
from pathlib import Path
from PIL import Image


def video_to_gif(video_path, gif_path, width=720, frame_step=3):
    cap = cv2.VideoCapture(str(video_path))
    source_fps = cap.get(cv2.CAP_PROP_FPS) or 30
    frames = []
    i = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if i % frame_step == 0:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w = frame.shape[:2]
            frame = cv2.resize(frame, (width, int(h * width / w)), interpolation=cv2.INTER_AREA)
            frames.append(Image.fromarray(frame))
        i += 1

    cap.release()

    if not frames:
        print("No frames read. Check the video path.")
        return

    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / (source_fps / frame_step)),
        loop=0,
        optimize=True,
    )
    print(f"{gif_path}: {len(frames)} frames, {gif_path.stat().st_size / 1_048_576:.1f} MB")


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]
    media_dir = repo_root / "docs" / "media"
    media_dir.mkdir(parents=True, exist_ok=True)

    video = Path(r"C:\Users\DM77\Downloads\auth_demo.mp4")
    video_to_gif(video, media_dir / "auth_demo.gif", width=600, frame_step=6)