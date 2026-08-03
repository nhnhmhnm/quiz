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


def handle_quiz_management(state):
    changed = False

    while True:
        quizzes = list_quizzes(state)
        print_quiz_management_menu(quizzes)
        choice = input("선택: ").strip().upper()

        if choice == "A":
            question = input("문제를 입력하세요: ").strip()
            answer = input("정답을 입력하세요: ").strip()
            try:
                add_quiz(state, question, answer)
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
            name = input("조회할 이름을 입력하세요: ").strip()
            records = get_personal_history(state, name)
            print(f"\n[{name or 'UNKNOWN'}님의 기록]")
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
