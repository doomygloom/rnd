import cv2
import time

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # use find_all_cameras.py to find your camera index (0 in this instance)

    if not cap.isOpened():
        print("Error: Could not open video device.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("Camera opened successfully.")
    print("Controls: [q] Quit | [f] Toggle FPS | [s] Save Snapshot | [r] Start/Stop Recording | [g] Toggle Grayscale")

    show_fps = False
    recording = False
    grayscale = False
    out = None
    last_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab a frame.")
            break

        if grayscale:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        if show_fps:
            current_time = time.time()
            fps = 1 / (current_time - last_time)
            last_time = current_time
            cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if recording and out is not None:
            out.write(frame)

        cv2.imshow('Live Camera Feed', frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('f'):
            show_fps = not show_fps
            print(f"Show FPS: {show_fps}")
        elif key == ord('g'):
            grayscale = not grayscale
            print(f"Grayscale mode: {grayscale}")
        elif key == ord('s'):
            filename = f'snapshot_{int(time.time())}.png'
            cv2.imwrite(filename, frame)
            print(f"Saved snapshot as {filename}")
        elif key == ord('r'):
            if not recording:
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(f'recording_{int(time.time())}.avi', fourcc, 20.0, (640, 480))
                recording = True
                print("Started recording.")
            else:
                recording = False
                out.release()
                out = None
                print("Stopped recording.")

    cap.release()
    if out is not None:
        out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
