import cv2

intput_video = 'intput.mp4'
output_video = 'input.mp4'

cap = cv2.VideoCapture(intput_video)

# Define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter(output_video,fourcc, 30.0, (1280, 720))

while True:
    # Grab a single frame of video
    ret, frame = cap.read()
    if ret:
        frame = frame[0:720, 0:1280] # [rows, cols]

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
