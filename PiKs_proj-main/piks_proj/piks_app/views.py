from django.shortcuts import render
# from piks_app.webcam import main
import cv2
import tkinter as tk
from PIL import ImageTk, Image
import os

# Create your views here.

def index(request):
    return render(request, 'index.html')

def webcam(request):
    curr_index = 0  # curr_index 변수를 main 함수 내에 선언

    def capture_image():
        # 웹캠 프레임 캡처
        nonlocal curr_index  # curr_index 변수를 nonlocal로 선언
        ret, frame = cap.read()
        path = os.path.join(img_paths,img_list[curr_index])
        bg_img = cv2.imread(path)
        # 이미지 저장    
        cv2.imwrite('./save/original.jpg', bg_img)
        cv2.imwrite('./save/captured.jpg', frame)
        exit_program()
        
    def exit_program():
        # 프로그램 종료
        cap.release()
        cv2.destroyAllWindows()
        root.quit()

    def blend_images(bg_img, frame):
        # 배경 이미지와 현재 프레임을 합성
        bg_img = cv2.resize(bg_img, (frame.shape[1], frame.shape[0]))
        result = cv2.addWeighted(bg_img, 0.2, frame, 0.8, 0)
        return result

    def show_previous_image():
        # 이전 이미지로 전환
        nonlocal curr_index  # curr_index 변수를 nonlocal로 선언
        curr_index = (curr_index - 1) % len(img_list)
        update_background()
        
    def show_next_image():
        # 다음 이미지로 전환
        nonlocal curr_index  # curr_index 변수를 nonlocal로 선언
        curr_index = (curr_index + 1) % len(img_list)
        update_background()

    def update_background():
        #  배경 이미지 업데이트
        if is_edge_mode:
            path = os.path.join(img_paths_edge, img_list_edge[curr_index])
            bg_img = cv2.imread(path)
        else:
            path = os.path.join(img_paths, img_list[curr_index])
            bg_img = cv2.imread(path)
        
        bg_img = cv2.resize(bg_img, (frame_width, frame_height))
        return bg_img

    def background_original():
        nonlocal is_edge_mode
        is_edge_mode = False
        
        ret, frame = cap.read()
        
        bg_img = update_background()
        
        # 프레임과 배경 이미지 합성
        result = blend_images(bg_img, frame)
        
        # 합성된 이미지를 PIL 이미지로 변환
        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        result = Image.fromarray(result)
        result = ImageTk.PhotoImage(result)
        
        # 라벨에 이미지 업데이트
        video_label.configure(image=result)
        video_label.image = result
        
    def background_edge():
        nonlocal is_edge_mode
        is_edge_mode = True
        
        path = os.path.join(img_paths_edge, img_list_edge[curr_index])
        bg_img = cv2.imread(path)
        bg_img = cv2.resize(bg_img, (frame_width, frame_height))
        
        ret, frame = cap.read()

        # 프레임과 배경 이미지 합성
        result = blend_images(bg_img, frame)
        
        # 합성된 이미지를 PIL 이미지로 변환
        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        result = Image.fromarray(result)
        result = ImageTk.PhotoImage(result)
        
        # 라벨에 이미지 업데이트
        video_label.configure(image=result)
        video_label.image = result

    def show_frame():
        # 웹캠 프레임 읽기
        ret, frame = cap.read()
        
        bg_img = update_background()
        
        # 프레임과 배경 이미지 합성
        result = blend_images(bg_img, frame)
        
        # 합성된 이미지를 PIL 이미지로 변환
        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        result = Image.fromarray(result)
        result = ImageTk.PhotoImage(result)

        # 라벨에 이미지 업데이트
        video_label.configure(image=result)
        video_label.image = result

        # 지속적으로 프레임 업데이트
        video_label.after(10, show_frame)

    # 웹캠 캡처 객체 생성
    cap = cv2.VideoCapture(0)

    # Tkinter 윈도우 생성
    root = tk.Tk()
    root.title("Webcam with Button")
    root.geometry("840x625")

    # 웹캠 이미지를 보여주기 위한 라벨
    video_label = tk.Label(root)
    video_label.pack()

    # 배경 이미지 기본 로드
    img_paths = "./piks_app/image/grid/0"
    img_list = os.listdir(img_paths)

    img_paths_edge = './piks_app/image/grid/0_edge'
    img_list_edge = os.listdir(img_paths_edge)
        
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    is_edge_mode = False
    update_background()

    # 종료 버튼
    exit_button = tk.Button(root, text="종료", command=exit_program)
    exit_button.pack(side=tk.BOTTOM, pady=10)

    # 캡처 버튼
    capture_button = tk.Button(root, text="사진캡쳐", command=capture_image)
    capture_button.pack(side=tk.BOTTOM, pady=10)

    # 왼쪽 버튼
    previous_button = tk.Button(root, text="이전 이미지", command=show_previous_image)
    previous_button.pack(side=tk.LEFT, padx=10)

    # 오른쪽 버튼
    next_button = tk.Button(root, text="다음 이미지", command=show_next_image)
    next_button.pack(side=tk.LEFT, padx=10)

    # edge 버튼
    next_button = tk.Button(root, text="선 이미지", command=background_edge)
    next_button.pack(side=tk.RIGHT, padx=5)
    # 기본 버튼
    previous_button = tk.Button(root, text="원본 이미지", command=background_original)
    previous_button.pack(side=tk.RIGHT, padx=5)

    # 프레임 업데이트 시작
    show_frame()

    # Tkinter 이벤트 루프 시작
    root.mainloop()
    return render(request, 'index.html')
