import pandas as pd
import tkinter as tk
from tkinter import messagebox

# 비정형.xlsx 파일을 불러오는 함수
def load_data():
    return pd.read_excel('비정형.xlsx', engine='openpyxl')

# 소모품.xlsx 파일을 불러오는 함수
def load_material_data():
    return pd.read_excel('소모품.xlsx', engine='openpyxl')

# 비정형 검색기 기능
def show_unstructured_search():
    clear_frame()

    # 검색어 입력 라벨 및 엔트리 생성
    entry_frame = tk.Frame(frame)
    entry_frame.pack(pady=5)

    label1 = tk.Label(entry_frame, text="검색어 1:")
    label1.grid(row=0, column=0, padx=5)

    global entry1
    entry1 = tk.Entry(entry_frame, width=20)
    entry1.grid(row=0, column=1, padx=5)

    label2 = tk.Label(entry_frame, text="검색어 2:")
    label2.grid(row=0, column=2, padx=5)

    global entry2
    entry2 = tk.Entry(entry_frame, width=20)
    entry2.grid(row=0, column=3, padx=5)

    label3 = tk.Label(entry_frame, text="검색어 3:")
    label3.grid(row=0, column=4, padx=5)

    global entry3
    entry3 = tk.Entry(entry_frame, width=20)
    entry3.grid(row=0, column=5, padx=5)

    # 검색 버튼 배치
    search_button = tk.Button(entry_frame, text="검색", command=search)
    search_button.grid(row=0, column=6, padx=5)

    # 검색 결과 리스트 박스
    global listbox
    listbox = tk.Listbox(frame, width=150, height=15)
    listbox.pack(pady=5)

    # 뒤로가기 버튼
    back_button = tk.Button(frame, text="뒤로가기", command=show_main_menu)
    back_button.pack(pady=5)

def show_material_search():
    clear_frame()
    label = tk.Label(frame, text="재료 검색어 입력:")
    label.pack(pady=5)

    material_entry = tk.Entry(frame, width=50)
    material_entry.pack(pady=5)

    material_search_button = tk.Button(frame, text="재료 검색", command=lambda: material_search(material_entry.get()))
    material_search_button.pack(pady=5)

    global material_listbox
    material_listbox = tk.Listbox(frame, width=100, height=12)
    material_listbox.pack(pady=5)

    back_button = tk.Button(frame, text="뒤로가기", command=show_main_menu)
    back_button.pack(pady=5)

def material_search(term):
    material_data = load_material_data()
    
    if term.strip() == "":
        messagebox.showwarning("경고", "검색어를 입력해주세요.")
        return

    # A열과 B열에서 검색어 포함된 항목 찾기
    filtered_materials = material_data[material_data.apply(lambda row: row.astype(str).str.contains(term).any(), axis=1)]

    material_listbox.delete(0, tk.END)  # 리스트 박스 초기화

    if not filtered_materials.empty:
        for index, row in filtered_materials.iterrows():
            material_listbox.insert(tk.END, f"검색어: {row[0]}, 파밍: {row[1]}")
    else:
        material_listbox.insert(tk.END, "결과 없음")

def search():
    keyword1 = entry1.get().strip()
    keyword2 = entry2.get().strip()
    keyword3 = entry3.get().strip()

    if not keyword1 and not keyword2 and not keyword3:
        messagebox.showwarning("경고", "최소 하나의 검색어를 입력해주세요.")
        return

    # 검색어가 포함된 행 찾기
    conditions = []
    if keyword1:
        conditions.append(data.apply(lambda row: row.astype(str).str.contains(keyword1).any(), axis=1))
    if keyword2:
        conditions.append(data.apply(lambda row: row.astype(str).str.contains(keyword2).any(), axis=1))
    if keyword3:
        conditions.append(data.apply(lambda row: row.astype(str).str.contains(keyword3).any(), axis=1))

    # 모든 키워드가 포함된 항목 찾기
    if conditions:
        combined_condition = conditions[0]
        for condition in conditions[1:]:
            combined_condition &= condition

        filtered_data = data[combined_condition]

        if not filtered_data.empty:
            # G 열을 기준으로 정렬 (내림차순)
            filtered_data = filtered_data.sort_values(by=filtered_data.columns[6], ascending=False)  # G 열이 7번째 열이므로 인덱스는 6
            results = filtered_data.iloc[:, 0].tolist()  # 첫 번째 열의 결과만 가져옴
            items = filtered_data.iloc[:, 1:].apply(lambda row: ', '.join(row.dropna().astype(str)), axis=1).tolist()
        else:
            # 모든 키워드가 포함된 항목이 없을 경우 최대한 겹치는 항목 찾기
            all_conditions = [data.apply(lambda row: row.astype(str).str.contains(keyword).any(), axis=1) for keyword in [keyword1, keyword2, keyword3] if keyword]
            fallback_condition = all_conditions[0]
            for cond in all_conditions[1:]:
                fallback_condition |= cond
            
            filtered_data = data[fallback_condition]
            results = filtered_data.iloc[:, 0].tolist() if not filtered_data.empty else ["결과 없음"]
            items = filtered_data.iloc[:, 1:].apply(lambda row: ', '.join(row.dropna().astype(str)), axis=1).tolist() if not filtered_data.empty else [""]

            # G 열을 기준으로 정렬 (내림차순)
            filtered_data = filtered_data.sort_values(by=filtered_data.columns[6], ascending=False)

        # 검색 키워드에 해당되지 않는 아이템 목록 제거
        filtered_items = []
        for item in items:
            relevant_items = [i for i in item.split(', ') if keyword1 in i or keyword2 in i or keyword3 in i]
            filtered_items.append(', '.join(relevant_items) if relevant_items else "없음")

        listbox.delete(0, tk.END)
        for result, item in zip(results, filtered_items):
            listbox.insert(tk.END, f"{result}: {item}")  # 아이템 목록 함께 출력
    else:
        listbox.delete(0, tk.END)
        listbox.insert(tk.END, "결과 없음")

# 프레임 초기화
def clear_frame():
    for widget in frame.winfo_children():
        widget.destroy()

# 메인 메뉴로 돌아가는 함수
def show_main_menu():
    clear_frame()
    
    # 이미지 로드
    main_image = tk.PhotoImage(file='amorphous material.png')  # 버튼에 사용할 이미지 파일 경로
    main_image2 = tk.PhotoImage(file='basic_materials.png')  # 버튼에 사용할 이미지 파일 경로
    main_image3 = tk.PhotoImage(file='successor.png')  # 버튼에 사용할 이미지 파일 경로

    unstructured_button = tk.Button(frame, text="비정형 검색", image=main_image, compound=tk.TOP, command=show_unstructured_search)
    unstructured_button.image = main_image  # 이미지 참조 유지
    unstructured_button.pack(side=tk.RIGHT, padx=10)

    material_button = tk.Button(frame, text="재료 검색", image=main_image2, compound=tk.TOP, command=show_material_search)
    material_button.image = main_image2  # 이미지 참조 유지
    material_button.pack(side=tk.RIGHT, padx=10)

    # 캐릭터 버튼 추가
    character_button = tk.Button(frame, text="계승자", image=main_image3, compound=tk.TOP, command=show_character_search)
    character_button.image = main_image3  # 이미지 참조 유지
    character_button.pack(side=tk.LEFT, padx=10)
    

def show_character_search():
    clear_frame()
    label = tk.Label(frame, text="캐릭터 검색 기능은 아직 구현되지 않았습니다.")
    label.pack(pady=20)

    back_button = tk.Button(frame, text="뒤로가기", command=show_main_menu)
    back_button.pack(pady=5)
    
    
# 데이터 로드
data = load_data()

# UI 설정
root = tk.Tk()
root.title("비정형 검색기")

frame = tk.Frame(root)
frame.pack(pady=20)

# 초기 화면에 버튼 생성
show_main_menu()

# GUI 실행
root.mainloop()

# def show_main_menu():
#     clear_frame()
#     unstructured_button = tk.Button(frame, text="비정형 검색기", command=show_unstructured_search)
#     unstructured_button.pack(side=tk.LEFT, padx=10)

#     material_button = tk.Button(frame, text="재료 검색기", command=show_material_search)
#     material_button.pack(side=tk.LEFT, padx=10)

# # 데이터 로드
# data = load_data()

# # UI 설정
# root = tk.Tk()
# root.title("비정형 검색기")

# frame = tk.Frame(root)
# frame.pack(pady=20)

# # 초기 화면에 버튼 생성
# show_main_menu()

# # GUI 실행
# root.mainloop()
