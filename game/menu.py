from utils import prompt_input


# 퀴즈 목록 화면에서 문제와 정답을 한 줄로 요약해서 보여준다.
def _format_quiz_summary(quiz):
    answer_number = quiz["answer_index"]
    answer_text = quiz["choices"][answer_number - 1]
    return f'{quiz["question"]} / 정답: {answer_number}번 ({answer_text})'

    # 예전 주관식 형식은 더 이상 사용하지 않아 주석 처리했다.
    # return f'{quiz["question"]} / {quiz["answer"]}'


# 메인 메뉴 출력 전용 함수다.
def print_main_menu():
    print("\n========== QUIZ ==========")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 관리")
    print("3. 기록")
    print("4. 종료")
    print("==========================")


# 퀴즈 관리 메뉴에서 현재 등록된 문제와 선택지를 함께 보여준다.
def print_quiz_management_menu(quizzes):
    print("\n[등록된 퀴즈 목록]")

    if not quizzes:
        print("등록된 퀴즈가 없습니다.")
    else:
        for index, quiz in enumerate(quizzes, start=1):
            print(f"{index}. {_format_quiz_summary(quiz)}")

    print("\nA. 퀴즈 추가")
    print("D. 퀴즈 삭제")
    print("0. 돌아가기")


# 기록 관련 하위 메뉴 출력 전용 함수다.
def print_record_menu():
    print("\n1. 전체 랭킹 (TOP 3)")
    print("2. 개인 기록 조회")
    print("0. 돌아가기")


# 사용자가 결과를 읽고 다음 화면으로 넘어갈 시간을 주기 위한 일시정지다.
def pause():
    prompt_input("\n엔터를 누르면 계속합니다...")
