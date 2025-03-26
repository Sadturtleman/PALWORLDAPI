"""간단한 계산기 모듈입니다."""


def add_numbers(a, b):
    """두 숫자를 더한 결과를 반환합니다."""
    return a + b


def subtract_numbers(a, b):
    """두 숫자를 뺀 결과를 반환합니다."""
    return a - b


def multiply_numbers(a, b):
    """두 숫자를 곱한 결과를 반환합니다."""
    return a * b


def divide_numbers(a, b):
    """두 숫자를 나눈 결과를 반환합니다.

    Args:
        a (float): 분자
        b (float): 분모 (0이 아닌 숫자)

    Returns:
        float: 나눈 결과

    Raises:
        ValueError: b가 0일 경우
    """
    if b == 0:
        raise ValueError("분모는 0이 될 수 없습니다.")
    return a / b


def main():
    """메인 함수입니다. 간단한 예제를 실행합니다."""
    print("더하기:", add_numbers(2, 3))
    print("빼기:", subtract_numbers(5, 2))
    print("곱하기:", multiply_numbers(2, 4))
    print("나누기:", divide_numbers(10, 2))

def badFunction( ):
  return  1

if __name__ == "__main__":
    main()
