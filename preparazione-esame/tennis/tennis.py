"""
A game consists of a sequence of points played with the same player serving. A game is won by the first player to have
won at least four points in total and at least two points more than the opponent. The running score of each game is
described in a manner peculiar to tennis: scores from zero to three points are described as "love", "15", "30", and
"40", respectively. If at least three points have been scored by each player, making the player's scores equal at 40
apiece, the score is not called out as "40–40", but rather as "deuce". If at least three points have been scored by
each side and a player has one more point than his opponent, the score of the game is "advantage" for the player in the
lead. During informal games, advantage can also be called "ad in" or "van in" when the serving player is ahead, and
"ad out" or "van out" when the receiving player is ahead; alternatively, either player may simply call out "my ad" or
"your ad". The score of a tennis game during play is always read with the serving player's score first. In tournament
play, the chair umpire calls the point count (e.g., "15–love") after each point. At the end of a game, the chair umpire
also announces the winner of the game and the overall score.
"""


def print_header() -> str:
    return '''****************************
    * TENNIS GAME TRACKER - v1 *
    ****************************
    '''


def points_to_score(points: int) -> str:
    if points == 0:
        return "love"
    elif points == 1 or points == 2:
        return str(15 * points)
    return "40"


def win_string(points_s: int, points_r: int) -> str:
    if abs(points_s - points_r) >= 2:
        if points_s > points_r:
            return "End of the game: Serving player win!"
        else:
            return "End of the game: Receiving player win!"
    return ""


def running_score(points_s: int, points_r: int) -> str:
    to_return = "Running score:"
    if points_s == points_r:
        return f"{to_return} {points_to_score(points_s)}-all" if points_s < 3 else f"{to_return} deuce"
    if points_s >= 4 or points_r >= 4:
        return f"{to_return} ad-in" if points_s > points_r else f"{to_return} ad-out"
    return f"{to_return} {points_to_score(points_s)}-{points_to_score(points_r)}"


def running_score_or_win(points_s: int, points_r: int) -> str:
    win = ""
    if points_s >= 4 or points_r >= 4:
        win = win_string(points_s, points_r)
    return win if win != "" else running_score(points_s, points_r)


def take_input() -> str:
    user_input = input("Next point (S for serving player; R for receiving player): ").upper()
    while user_input not in ['R', 'S']:
        print("Wrong value ignored!")
        user_input = input("Next point (S for serving player; R for receiving player): ").upper()
    return user_input


def give_next_point(points: dict[str, int]) -> None:
    user_input = take_input()
    if user_input == 'S':
        points['S'] += 1
    elif user_input == 'R':
        points['R'] += 1


def game_loop(points: dict[str, int]) -> None:
    while True:
        score = running_score_or_win(points.get('S'), points.get('R'))
        print(score)
        if "End of the game" in score:
            return
        give_next_point(points)


def main() -> None:
    points = {
        'S': 0,
        'R': 0
    }
    print_header()
    game_loop(points)


if __name__ == '__main__':
    main()
