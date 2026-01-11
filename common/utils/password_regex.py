import re
PASSWORD_STRONG_REGEX = re.compile(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$'
)

# izoh: yuqoridagi regex:
# - kamida 1 kichik harf
# - kamida 1 katta harf
# - kamida 1 raqam
# - kamida 1 maxsus belgı (A-Za-z0-9 ga tegishli bo'lmagan)
# - jami uzunligi kamida 8
