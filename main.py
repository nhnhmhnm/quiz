from game import (
    add_quiz,
    delete_quiz,
    format_record,
    get_personal_history,
    get_top_rankings,
    list_quizzes,
    load_state,
    pause,
    play_quiz,
    print_main_menu,
    print_quiz_management_menu,
    print_record_menu,
    save_state,
)


# 퀴즈 관리 메뉴에서 문제 추가와 삭제를 반복 처리한다.
def handle_quiz_management(state):
    changed = False

    while True:
        quizzes = list_quizzes(state)
        print_quiz_management_menu(quizzes)
        choice = input("선택: ").strip().upper()

        if choice == "A":
            question = input("문제를 입력하세요: ").strip()
            choices = []
            for index in range(1, 5):
                choices.append(input(f"{index}번 보기를 입력하세요: ").strip())
            answer_index = input("정답 번호(1~4)를 입력하세요: ").strip()

            try:
                add_quiz(state, question, choices, answer_index)
                print("퀴즈가 추가되었습니다.")
                changed = True
            except ValueError as error:
                print(error)
            pause()
        elif choice == "D":
            if not quizzes:
                print("삭제할 퀴즈가 없습니다.")
                pause()
                continue

            raw_index = input("삭제할 문제 번호를 입력하세요: ").strip()
            try:
                deleted = delete_quiz(state, int(raw_index))
                print(f'퀴즈를 삭제했습니다: {deleted["question"]}')
                changed = True
            except (ValueError, IndexError):
                print("올바른 문제 번호를 입력해주세요.")
            pause()
        elif choice == "0":
            return changed
        else:
            print("지원하지 않는 메뉴입니다.")
            pause()


def _prompt_record_name():
    while True:
        name = input("조회할 이름을 입력하세요: ").strip()
        if name:
            return name
        print("이름은 비워둘 수 없습니다.")


# 저장된 랭킹과 개인 기록을 조회하는 메뉴다.
def show_records(state):
    while True:
        print_record_menu()
        choice = input("선택: ").strip()

        if choice == "1":
            records = get_top_rankings(state)
            print("\n[전체 랭킹]")
            if not records:
                print("기록이 없습니다.")
            else:
                for index, record in enumerate(records, start=1):
                    print(f"{index}. {format_record(record)}")
            pause()
        elif choice == "2":
            name = _prompt_record_name()
            records = get_personal_history(state, name)
            print(f"\n[{name}님의 기록]")
            if not records:
                print("일치하는 기록이 없습니다.")
            else:
                for index, record in enumerate(records, start=1):
                    print(f"{index}. {format_record(record)}")
            pause()
        elif choice == "0":
            return
        else:
            print("지원하지 않는 메뉴입니다.")
            pause()


# 프로그램 시작점으로, 메인 메뉴를 돌며 각 기능으로 분기한다.
def main():
    state = load_state()

    while True:
        print_main_menu()
        choice = input("선택: ").strip()

        if choice == "1":
            if play_quiz(state):
                save_state(state)
            pause()
        elif choice == "2":
            if handle_quiz_management(state):
                save_state(state)
        elif choice == "3":
            show_records(state)
        elif choice == "4":
            save_state(state)
            print("퀴즈 게임을 종료합니다.")
            break
        else:
            print("지원하지 않는 메뉴입니다.")
            pause()


if __name__ == "__main__":
    main()
