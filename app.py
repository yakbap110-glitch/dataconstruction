import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# 웹 페이지 기본 설정
st.set_page_config(page_title="정렬 알고리즘 시각화", page_icon="📊")
st.title("📊 정렬 알고리즘 시각화 앱")
st.write("원하는 정렬 알고리즘을 선택하고, 데이터가 어떻게 정렬되는지 확인해 보세요!")

# --- 세션 상태(Session State) 초기화 ---
# 버튼을 누를 때마다 데이터가 초기화되는 것을 방지하기 위해 데이터를 저장합니다.
if 'array' not in st.session_state:
    st.session_state.array = np.random.randint(1, 100, 20)

# --- 알고리즘 구현 (제너레이터 yield 사용) ---
# 배열의 상태가 바뀔 때마다 (배열, 강조할 인덱스1, 강조할 인덱스2)를 반환합니다.

def bubble_sort(arr):
    n = len(arr)
    arr_copy = arr.copy()
    for i in range(n):
        for j in range(0, n - i - 1):
            # 비교 중인 두 막대를 강조
            if arr_copy[j] > arr_copy[j + 1]:
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
            yield arr_copy, j, j + 1 

def selection_sort(arr):
    n = len(arr)
    arr_copy = arr.copy()
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            # 탐색 중인 막대를 강조
            yield arr_copy, min_idx, j
            if arr_copy[j] < arr_copy[min_idx]:
                min_idx = j
        arr_copy[i], arr_copy[min_idx] = arr_copy[min_idx], arr_copy[i]
        # 교환 후 강조
        yield arr_copy, i, min_idx

# --- 사이드바 설정 (컨트롤 패널) ---
st.sidebar.header("⚙️ 설정")
array_size = st.sidebar.slider("데이터 개수", 10, 50, 20)
animation_speed = st.sidebar.slider("애니메이션 속도 (초)", 0.01, 0.5, 0.1)
algo_choice = st.sidebar.selectbox("정렬 알고리즘 선택", ["버블 정렬 (Bubble Sort)", "선택 정렬 (Selection Sort)"])

# 새로운 데이터 생성 버튼
if st.sidebar.button("새로운 데이터 생성"):
    st.session_state.array = np.random.randint(1, 100, array_size)
    st.rerun() # 화면 새로고침

# --- 그래프 그리는 함수 ---
def draw_chart(arr, color_idx1=-1, color_idx2=-1):
    fig, ax = plt.subplots(figsize=(8, 4))
    # 기본 막대 색상은 파란색
    colors = ['#3498db'] * len(arr)
    
    # 비교하거나 교환하는 막대는 빨간색으로 강조
    if color_idx1 != -1: colors[color_idx1] = '#e74c3c'
    if color_idx2 != -1: colors[color_idx2] = '#e74c3c'
    
    ax.bar(range(len(arr)), arr, color=colors)
    ax.set_axis_off() # 깔끔하게 보이기 위해 x, y축 숨김
    return fig

# --- 메인 화면 ---
# 애니메이션이 들어갈 빈 공간(placeholder) 생성
chart_placeholder = st.empty()

# 초기 정렬 전 상태 보여주기
chart_placeholder.pyplot(draw_chart(st.session_state.array))

# 정렬 시작 버튼
if st.button("정렬 시작!", type="primary"):
    # 선택된 알고리즘의 제너레이터 가져오기
    if algo_choice == "버블 정렬 (Bubble Sort)":
        generator = bubble_sort(st.session_state.array)
    else:
        generator = selection_sort(st.session_state.array)
        
    # 제너레이터를 순회하며 애니메이션 효과 만들기
    for current_arr, idx1, idx2 in generator:
        fig = draw_chart(current_arr, idx1, idx2)
        chart_placeholder.pyplot(fig) # 그래프 덮어쓰기
        plt.close(fig) # 메모리 누수 방지를 위해 닫기
        time.sleep(animation_speed) # 속도 조절
        
    # 정렬이 끝난 후 최종 데이터를 세션 상태에 덮어쓰기
    st.session_state.array = current_arr
    
    # 모든 막대를 초록색으로 칠해 완료되었음을 알림
    fig_final, ax_final = plt.subplots(figsize=(8, 4))
    ax_final.bar(range(len(st.session_state.array)), st.session_state.array, color='#2ecc71')
    ax_final.set_axis_off()
    chart_placeholder.pyplot(fig_final)
    plt.close(fig_final)
    
    st.success("✨ 정렬이 완료되었습니다!")
