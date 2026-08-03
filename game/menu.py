def print_main_menu():
    print("\n========== QUIZ ==========")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 관리")
    print("3. 기록")
    print("4. 종료")
    print("==========================")


def print_quiz_management_menu(quizzes):
    print("\n[등록된 퀴즈 목록]")

    if not quizzes:
        print("등록된 퀴즈가 없습니다.")
    else:
        for index, quiz in enumerate(quizzes, start=1):
            print(f'{index}. {quiz["question"]} / {quiz["answer"]}')

    print("\nA. 퀴즈 추가")
    print("D. 퀴즈 삭제")
    print("0. 돌아가기")


def print_record_menu():
    print("\n1. 전체 랭킹 (TOP 3)")
    print("2. 개인 기록 조회")
    print("0. 돌아가기")


def pause():
    input("\n엔터를 누르면 계속합니다...")
